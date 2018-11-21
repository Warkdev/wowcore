from os import urandom
from Login.SRP import SRP


class Account(object):

    def __init__(self, name, password = None, salt = None, verifier = None):
        if not name:
            raise Exception('Account name should be specified!')

        self.name = name
        # password does not saves to DB
        self.password = password
        self.salt = salt
        self.verifier = verifier
        self.ip_addr = None
        # offset in minutes from UTC time
        self.timezone = None
        # operation system
        self.os = None
        self.platform = None
        self.locale = None

        if not password:
            if not salt or not verifier:
                raise Exception('Password does not exists! Password is necessary for SRP data generation')
        else:
            if not salt or not verifier:
                ' True when create account '
                self._generate_srp_data()
            elif salt and verifier:
                ' True when getting account from DB '
                self.salt = salt
                self.verifier = verifier

    def _generate_srp_data(self):
        self.salt = urandom(32)
        self.verifier = SRP._generate_verifier(
                self.name.upper(), 
                self.password.upper(), 
                self.salt)
