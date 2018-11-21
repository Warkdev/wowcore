from Server.BaseServer import BaseServer
from asyncio.streams import StreamReader, StreamWriter
from Logger.Logger import Logger
from Config.CONFIG import Connection
from Login.SessionStorage import session
from World.Auth.AuthSessionManager import AuthSessionManager
from Server.Queue.Queue import queue
from Server.Queue.QueueMessages import QueueMessages
import asyncio
from concurrent.futures import TimeoutError


class WorldServer(BaseServer):

    def __init__(self, host, port):
        super().__init__(host, port)
        self.connections = []

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        peername = writer.get_extra_info('peername')
        Logger.debug('[World Server]: Accept connection from {}'.format(peername))

        await self.accept_connection(peername)

        auth = AuthSessionManager(reader, writer)
        auth.prepare()
        await auth.process()

        # If I understand it correctly, after SMSG_AUTH_RESPONSE server should waiting for CMSG_CHAR_ENUM
        # But next request never sends by client. Client stucks on 'Connected'
        try:
            next_request = await asyncio.wait_for(reader.read(1024), timeout=1.0)
            Logger.debug('[World Server]: next request = {}'.format(next_request))
        except TimeoutError:
            Logger.error('[World Server]: next request was not received')
        finally:
            Logger.warning('[World Server]: closing...')

        #writer.close()

    async def accept_connection(self, peername):
        self.connections.append(peername)
        # currently do not in use
        await queue.put(QueueMessages.WORLD_SERVER_ACCEPT_CONNECTION.value)
        session.is_connection_accepted = True

    @staticmethod
    def create():
        Logger.info('[World Server]: init')
        return WorldServer(Connection.WORLD_SERVER_HOST.value, Connection.WORLD_SERVER_PORT.value)
