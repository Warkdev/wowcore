from Login.SRP import SRP
import base64
from Logger.Logger import Logger


class SessionStorage(object):

    ''' Stores information about current connection '''

    def __init__(self):
        self.current_account = None
        self.is_authenticated = False
        self.is_connection_accepted = False
        self.srp = SRP()
        self.recon_challenge = None
        self.auth_seed = None
        self.header_crypt = None
        Logger.error('Session generated')

    @property
    def session_key_as_bytes(self):
        return base64.b64decode(self.srp.session_key)

    @session_key_as_bytes.setter
    def session_key_as_bytes(self, value: bytes):
        self.srp.session_key = base64.b64encode(value).decode('ascii')


session = SessionStorage()
