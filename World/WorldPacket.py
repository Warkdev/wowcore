from struct import pack
from Login.SessionStorage import session


class WorldPacket(object):

    def __init__(self, opcode = None, data: bytes = None):
        self.opcode = opcode
        self.data = data

    def to_send(self):
        opcode_bytes = pack('<H', self.opcode)
        packet = opcode_bytes + self.data
        size_bytes = pack('>H', len(packet))
        packet = size_bytes + packet

        if session.header_crypt is not None:
            packet = session.header_crypt.encrypt(packet)

        return packet

    def to_recv(self, packet: bytes):
        if session.header_crypt:
            packet = session.header_crypt.decrypt(packet)

        size, self.opcode, self.packet = packet[0:2], packet[2:4], packet[4:]
        return size + self.opcode + self.packet