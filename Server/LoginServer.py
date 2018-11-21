from Server.BaseServer import BaseServer
from Login.AuthManager import AuthManager
from asyncio.streams import StreamReader, StreamWriter
from Logger.Logger import Logger
from Config.CONFIG import Connection


class LoginServer(BaseServer):

    def __init__(self, host, port):
        super().__init__(host, port)

    async def handle_connection(self, reader: StreamReader, writer: StreamWriter):
        peername = writer.get_extra_info('peername')
        Logger.info('[Login Server]: Accepted connection from {}'.format(peername))

        auth = AuthManager(reader, writer)

        while not reader.at_eof():
            response = await auth.process()
            if not response:
                break

        Logger.warning('[Login Server]: closing...')
        writer.close()

    @staticmethod
    def create():
        Logger.info('[Login Server]: init')
        return LoginServer(Connection.LOGIN_SERVER_HOST.value, Connection.LOGIN_SERVER_PORT.value)