from Login.SessionStorage import session
from asyncio.streams import StreamReader, StreamWriter
from os import urandom
from struct import pack, unpack
from World.WorldPacket import WorldPacket
from World.WorldOpCode import WorldOpCode
from Logger.Logger import Logger
from World.Auth.CONSTANTS import AUTH_SESSION_RESPONSE_CODES
from hashlib import sha1
from io import BytesIO
from World.Crypto.HeaderCrypt import HeaderCrypt
import asyncio
from concurrent.futures import TimeoutError


class AuthSessionManager(object):

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer
        self.data = bytes()
        self.build = 0
        self.unk = 0
        self.account_name = None
        self.client_seed = 0
        self.client_hash = bytes()
        self.session_key = bytes()
        self.server_hash = bytes()

    def prepare(self):
        # auth seed need to generate header_crypt
        auth_seed = int.from_bytes(urandom(4), 'little')
        session.auth_seed = auth_seed
        auth_seed_bytes = pack('<I', auth_seed)
        response = WorldPacket(WorldOpCode.SMSG_AUTH_CHALLENGE.value, auth_seed_bytes).to_send()
        self.writer.write(response)

    async def process(self):
        Logger.debug('[Auth Session Manager]: Trying to read packet')
        try:
            request = await asyncio.wait_for(self.reader.read(1024), timeout=1.0)

            self._parse_data(request)
            self._load_session_key()
            self._generate_server_hash()

            # NEXT PACKETS WILL BE ENCRYPTED
            self._setup_encryption()

            # SMSG_AUTH_RESPONSE encrypted, but client sends nothing and stucks on Connected

            if self.server_hash != self.client_hash:
                Logger.error('[Auth Session Manager]: Server hash is differs from client hash')
                return None
            else:
                # SMSG_AUTH_RESPONSE
                response = self._get_auth_response()
                self.writer.write(response)

                return response
        except TimeoutError:
            Logger.error('[Auth Session Manager]: Timeout...')
            return None

    def _parse_data(self, data: bytes):
        # omit first 6 bytes, cause 01-02 = packet size, 03-04 = opcode (0x1ED), 05-06 - unknown null-bytes
        tmp_buf = BytesIO(data[6:])
        self.build = unpack('<H', tmp_buf.read(2))[0]
        # remove next 6 unknown null-bytes (\x00)
        tmp_buf.read(6)
        self.account_name = self._parse_account_name(tmp_buf)

        self.client_seed = tmp_buf.read(4)
        self.client_hash = tmp_buf.read(20)

    def _generate_server_hash(self):
        Logger.info('[Auth Session Manager]: generating server hash')
        auth_seed = session.auth_seed
        del session.auth_seed
        to_hash = (
            self.account_name.encode('ascii') +
            bytes(4) +
            self.client_seed +
            int.to_bytes(auth_seed, 4, 'little') +
            self.session_key
        )
        self.server_hash = sha1(to_hash).digest()

    def _load_session_key(self):
        Logger.info('[Auth Session Manager]: loading session key')
        self.session_key = session.session_key_as_bytes

    def _setup_encryption(self):
        Logger.info('[Auth Session Manager]: setup encryption')
        try:
            session.header_crypt = HeaderCrypt(self.session_key)
        except Exception as e:
            Logger.error('[Auth Session Manager]: {}'.format(e))

    def _parse_account_name(self, buffer: BytesIO):
        Logger.info('[Auth Session Manager]: parsing account name')
        result = bytes()

        while True:
            char = buffer.read(1)
            if char and char != b'\x00':
                result += char
            else:
                break

        return result.decode('ascii')

    def _get_auth_response(self):
        # updating session request
        response = pack('<BIBIB',
                        AUTH_SESSION_RESPONSE_CODES.AUTH_OK.value,
                        0x00,  # BillingTimeRemaining
                        0x00,  # BillingPlanFlags
                        0x00,  # BillingTimeRested
                        0x01   # Expansion, 0 - normal, 1 - TBC, must be set manually for each account
        )

        packet = WorldPacket(
            WorldOpCode.SMSG_AUTH_RESPONSE.value,
            response
        ).to_send()

        Logger.info('[Auth Session Manager]: sending SMSG_AUTH_RESPONSE')

        return packet
