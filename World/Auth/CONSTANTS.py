from enum import Enum


class AUTH_SESSION_STATES(Enum):

    INIT                        = 0x00
    AUTH_OK                     = 0x02  # Session encrypt key exists + client at char screen
    IN_WORLD                    = 0x03


class AUTH_SESSION_RESPONSE_CODES(Enum):

    AUTH_OK                     = 0x0C
    AUTH_FAILED                 = 0x0D
    AUTH_REJECT                 = 0x0E
    AUTH_BAD_SERVER_PROOF       = 0x0F
    AUTH_UNAVAILABLE            = 0x10
    AUTH_SYSTEM_ERROR           = 0x11
    AUTH_BILLING_ERROR          = 0x12
    AUTH_BILLING_EXPIRED        = 0x13
    AUTH_VERSION_MISMATCH       = 0x14
    AUTH_UNKNOWN_ACCOUNT        = 0x15
    AUTH_INCORRECT_PASSWORD     = 0x16
    AUTH_SESSION_EXPIRED        = 0x17
    AUTH_SERVER_SHUTTING_DOWN   = 0x18
    AUTH_ALREADY_LOGGING_IN     = 0x19
    AUTH_LOGIN_SERVER_NOT_FOUND = 0x1A
    AUTH_WAIT_QUEUE             = 0x1B
    AUTH_BANNED                 = 0x1C
    AUTH_ALREADY_ONLINE         = 0x1D
    AUTH_NO_TIME                = 0x1E
    AUTH_DB_BUSY                = 0x1F
    AUTH_SUSPENDED              = 0x20
    AUTH_PARENTAL_CONTROL       = 0x21
