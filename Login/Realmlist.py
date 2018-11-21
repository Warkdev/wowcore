from struct import pack
from Login.LoginOpCode import LoginOpCode
from World.Realmlist.Sandbox.Sandbox import realm
from Realm.CONSTANTS import RealmPopulation, RealmFlags
from Logger.Logger import Logger


class Realmlist(object):

    REALMLIST_RESPONSE_HEADER_FORMAT = '<BHIH'
    REALMLIST_RESPONSE_FOOTER_FORMAT = '<B'
    MIN_RESPONSE_SIZE = 7

    def __init__(self, data = None):
        self.packet = data

    def process(self):
        return self._get_response()

    def _get_response(self):
        Logger.debug('[Realmlist]: processing')

        realm_packet = realm.get_state_packet(RealmFlags.NORMAL.value, RealmPopulation.LOW.value)
        realm_packet_as_bytes = b''.join([realm_packet])

        num_realms = 1

        header = pack(Realmlist.REALMLIST_RESPONSE_HEADER_FORMAT,
                      LoginOpCode.REALMLIST.value,
                      Realmlist.MIN_RESPONSE_SIZE + len(realm_packet_as_bytes),
                      0x00,
                      num_realms
                      )

        footer = pack(Realmlist.REALMLIST_RESPONSE_FOOTER_FORMAT, 0)

        response = header + realm_packet_as_bytes + footer

        return response
