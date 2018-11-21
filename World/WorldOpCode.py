from enum import Enum


class WorldOpCode(Enum):

    SMSG_AUTH_CHALLENGE      = 0x1EC
    CMSG_AUTH_SESSION        = 0x1ED
    SMSG_AUTH_RESPONSE       = 0x1EE
    SMSG_ADDON_INFO          = 0x2EF
    SMSG_CLIENTCACHE_VERSION = 0x4AB
    SMSG_TUTORIAL_FLAGS      = 0x0FD
    SMSG_REALM_SPLIT         = 0x38B
    SMSG_ACCOUNT_DATA_TIMES  = 0x209
    CMSG_CHAR_CREATE         = 0x036
    CMSG_CHAR_ENUM           = 0x037
    CMSG_CHAR_DELETE         = 0x038
    SMSG_CHAR_CREATE         = 0x03A
    SMSG_CHAR_ENUM           = 0x03B
    SMSG_CHAR_DELETE         = 0x03C
    CMSG_PLAYER_LOGIN        = 0x03D
    CMSG_PING                = 0x1DC
    SMSG_PONG                = 0x1DD
