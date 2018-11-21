from Logger.Logger import Logger


class HeaderCrypt(object):

    ENCRYPT_HEADER_SIZE = 4
    DECRYPT_HEADER_SIZE = 6

    def __init__(self, session_key):
        self.session_key = session_key
        self.send_i = 0
        self.send_j = 0
        self.recv_i = 0
        self.recv_j = 0

    def encrypt(self, data):
        assert len(data) >= HeaderCrypt.ENCRYPT_HEADER_SIZE
        encrypted_header = [0] * HeaderCrypt.ENCRYPT_HEADER_SIZE

        for index in range(HeaderCrypt.ENCRYPT_HEADER_SIZE):
            enc = (data[index] ^ self.session_key[self.send_i]) + self.send_j
            enc %= 0x100
            encrypted_header[index] = self.send_j = enc
            self.send_i = (self.send_i + 1) % len(self.session_key)

        return bytes(encrypted_header) + data[HeaderCrypt.ENCRYPT_HEADER_SIZE:]

    def decrypt(self, data):
        assert len(data) >= HeaderCrypt.DECRYPT_HEADER_SIZE
        decrypted_header = [0] * HeaderCrypt.DECRYPT_HEADER_SIZE

        for index in range(self.DECRYPT_HEADER_SIZE):
            dec = (data[index] - self.recv_j) ^ self.session_key[self.recv_i]
            dec %= 0x100
            decrypted_header[index] = dec
            self.recv_j = data[index]
            self.recv_i = (self.recv_i + 1) % len(self.session_key)

        return bytes(decrypted_header) + data[HeaderCrypt.DECRYPT_HEADER_SIZE:]
