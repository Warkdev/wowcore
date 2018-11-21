from struct import unpack, pack, error as StructError
from Logger.Logger import Logger
from Login.LoginOpCode import LoginOpCode, LoginResult
from Login.SessionStorage import session


class LoginProof(object):

    LOGIN_PROOF_FORMAT = '<32s20s20sBx'

    def __init__(self, data: bytes):
        self.packet = data
        self.client_ephemeral = 0
        self.client_proof = bytes()
        self.checksum = bytes()
        self.unk = 0

    def process(self):
        Logger.debug('[Login Proof]: processing...')
        self._parse_data()

        session.srp.generate_session_key(self.client_ephemeral, session.current_account.verifier)
        session.srp.generate_client_proof(self.client_ephemeral, session.current_account)

        session.is_authenticated = False

        if session.srp.client_proof == self.client_proof:
            Logger.debug('[Login Proof]: OK')
            session.srp.generate_server_proof(self.client_ephemeral)

            # generate for server-side authentication (next step, after realmlist recv)
            session.session_key_as_bytes = session.srp.session_key
            # additional checking for World Server
            session.is_authenticated = True

            return self._get_response()

        return None

    def _parse_data(self):
        try:
            parsed_data = unpack(LoginProof.LOGIN_PROOF_FORMAT, self.packet)
            self.client_ephemeral = int.from_bytes(parsed_data[0], 'little')
            self.client_proof = parsed_data[1]
            self.checksum = parsed_data[2]
            self.unk = parsed_data[3]
        except StructError as e:
            Logger.error('[Login Proof]: on unpacking data(len={}), error={}'.format(len(self.packet), StructError))

    def _get_response(self):
        try:
            response = pack('<2B20sQ2B',
                            LoginOpCode.LOGIN_PROOF.value,
                            LoginResult.SUCCESS.value,
                            session.srp.server_proof,
                            0x00800000,  # unk1
                            0x00,        # unk2
                            0x00         # unk3
            )
        except Exception as e:
            Logger.error('[Login Proof]: {}'.format(e))
        else:
            return response
