from enum import Enum


class Connection(Enum):
    # connection still works if I change login host and port
    # does it necessary to keep this default settings ?
    LOGIN_SERVER_HOST = '0.0.0.0'
    LOGIN_SERVER_PORT = 3724

    WORLD_SERVER_HOST = '127.0.0.1'
    WORLD_SERVER_PORT = 8085

    REALM_NAME        = 'Sandbox'
    REALM_HOST        = '127.0.0.1'
    REALM_PORT        = 8085

    # do not forget create databases from DB/DB_List.py
    # in future auto db creating script will be added
    # Also see DB/Fixtures folder for some tables with predefined data
    DB_HOST           = '127.0.0.1'
    DB_USER           = 'wowdb'
    DB_PASSWORD       = 'wowdb'
