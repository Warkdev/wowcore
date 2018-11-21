from Login.SRP import SRP
from struct import unpack, pack, error as StructError
from Login.LoginOpCode import LoginOpCode, LoginResult
from Logger.Logger import Logger
from os import urandom
from Account.AccountManager import AccountManager
from Login.SessionStorage import session


class LoginChallenge(object):

    LOGIN_CHAL_PACKET_FORMAT = '<BBx3sBBBBH3sB3sx4sBHBBBBBB%ds'
    PACKET_SIZE_WITHOUT_ACC_NAME = 33

    def __init__(self, data: bytes):
        self.packet = data
        self.unk_code = 0
        self.size = 0
        self.game_name = None
        self.version_major = 0
        self.version_minor = 0
        self.version_patch = 0
        self.version_build = 0
        self.os = None
        self.platform = None
        self.locale = None
        self.timezone = 0
        self.ip_addr = (0, 0, 0, 0)
        self.account_name_size = 0
        self.account_name = None

    def process(self):
        Logger.debug('[Login Challenge]: processing')
        self._parse_data()

        try:
            current_account = AccountManager.get_account(self.account_name)

            if current_account is None:
                raise Exception('Account \'{}\' is not found'.format(self.account_name))

            current_account.os = self.os
            current_account.ip_addr = '.'.join([str(i) for i in self.ip_addr])
            current_account.platform = self.platform
            current_account.timezone = self.timezone
            current_account.locale = self.locale

            AccountManager.update_account(current_account)

            session.current_account = current_account

        # TODO: define account exceptions
        except Exception as e:
            Logger.error('[Login Challenge]: {}'.format(e))
            return None
        finally:
            return self._get_response()

    def _parse_data(self):
        def _decode_cstring(cstring, encoding='ascii'):
            if type(cstring) is bytes:
                return cstring.decode(encoding).strip('\x00')[::-1]
            else:
                return cstring
        try:
            # remaining part of packet, that contains account name and byte with size of it
            packet_part_with_acc = (len(self.packet) - LoginChallenge.PACKET_SIZE_WITHOUT_ACC_NAME)
            parsed_data = unpack(LoginChallenge.LOGIN_CHAL_PACKET_FORMAT % packet_part_with_acc, self.packet)

            self.unk_code = parsed_data[0]
            self.size = parsed_data[1]
            self.game_name = _decode_cstring(parsed_data[2])
            self.version_major = parsed_data[4]
            self.version_minor = parsed_data[5]
            self.version_patch = parsed_data[6]
            self.version_build = parsed_data[7]
            self.platform = _decode_cstring(parsed_data[8])
            self.os = _decode_cstring(parsed_data[10])
            self.locale = _decode_cstring(parsed_data[11])
            self.timezone = parsed_data[12]
            self.ip_addr = parsed_data[15:19]
            self.account_name_size, account_name = parsed_data[19:]
            self.account_name = account_name.decode('ascii')
        except UnicodeDecodeError as e:
            Logger.error('[Login Challenge]: UnicodeDecodeError: {}'.format(e))

        except StructError as e:
            Logger.error('[Login Challenge]: StructError: {}'.format(e))

        except Exception as e:
            Logger.error('[Login Challenge]: exception({})'.format(e.__class__))

    def _get_response(self):
        session.srp.generate_server_ephemeral(session.current_account.verifier)

        generator = int.to_bytes(SRP.GENERATOR, 1, 'little')
        modulus = int.to_bytes(SRP.MODULUS, 32, 'little')
        server_eph = int.to_bytes(session.srp.serv_ephemeral, 32, 'little')

        response = pack('<3B32sB1sB32s32s16sB',
                        LoginOpCode.LOGIN_CHALL.value,
                        0,
                        LoginResult.SUCCESS.value,
                        server_eph,
                        len(generator),
                        generator,
                        len(modulus),
                        modulus,
                        session.current_account.salt,
                        urandom(16),
                        0  # ?
        )

        return response
