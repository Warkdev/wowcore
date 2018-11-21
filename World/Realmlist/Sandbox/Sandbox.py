from Realm.Realm import Realm
from Config.CONFIG import Connection
from Realm.CONSTANTS import RealmType

realm = Realm(
    Connection.REALM_NAME.value,
    Connection.REALM_HOST.value,
    Connection.REALM_PORT.value,
    RealmType.NORMAL.value
)