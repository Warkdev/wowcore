from struct import pack, unpack
from Logger.Logger import Logger
from Login.LoginOpCode import LoginOpCode, LoginResult
from os import urandom
from Login.SessionStorage import session


class ReconChallenge(object):
    # same format with Login Challenge
    RECON_CHAL_PACKET_FORMAT = '<BBx3sBBBBH3sB3sx4sBHBBBBBB%ds'
    PACKET_SIZE_WITHOUT_ACC_NAME = 33

    def __init__(self, data: bytes):
        self.packet = data
        self.unk_code = 0
        self.size = 0
        self.account_name_size = 0
        self.account_name = None

    def process(self):
        Logger.info('[Recon Challenge]: processing...')
        self._parse_data()
        return self._get_response()

    def _parse_data(self):
        # remaining part of packet, that contains account name and byte with size of it
        packet_part_with_acc = (len(self.packet) - ReconChallenge.PACKET_SIZE_WITHOUT_ACC_NAME)
        parsed_data = unpack(ReconChallenge.RECON_CHAL_PACKET_FORMAT % packet_part_with_acc, self.packet)
        self.unk_code = parsed_data[0]
        self.size = parsed_data[1]
        self.account_name_size, account_name = parsed_data[19:]
        self.account_name = account_name.decode('ascii')

    def _get_response(self):
        session.recon_challenge = urandom(16)

        response = pack('<2B16s2B',
                        LoginOpCode.RECON_CHALL.value,
                        LoginResult.SUCCESS.value,
                        session.recon_challenge,
                        0,
                        0
                        )

        return response
