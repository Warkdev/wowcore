from enum import Enum


class QueueMessages(Enum):

    WORLD_SERVER_REFUSE_CONNECTION = 0x00
    WORLD_SERVER_ACCEPT_CONNECTION = 0x01
