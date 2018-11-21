from asyncio.streams import StreamReader, StreamWriter
from Login.LoginChallenge import LoginChallenge
from Login.LoginProof import LoginProof
from Login.Realmlist import Realmlist
from Login.ReconChallenge import ReconChallenge
from Logger.Logger import Logger
import asyncio
from concurrent.futures import TimeoutError


class AuthManager(object):

    AUTH_HANDLERS = {
        0x00: LoginChallenge,
        0x01: LoginProof,
        0x02: ReconChallenge,
        0x03: 'ReconProof',
        0x10: Realmlist
    }

    def __init__(self, reader: StreamReader, writer: StreamWriter):
        self.reader = reader
        self.writer = writer

    async def process(self):
        try:
            request = await asyncio.wait_for(self.reader.read(1024), timeout=0.5)
            if request:
                opcode, packet = request[0], request[1:]
                handler = AuthManager.AUTH_HANDLERS[opcode]
                response = handler(packet).process()

                if response:
                    Logger.debug('[Auth Manager]: sending response back to client...')
                    self.writer.write(response)

                return response
            else:
                Logger.error('[Auth Manager]: no request was received')
                return None

        except TimeoutError:
            Logger.error('[AuthManager]: Timeout')
            return None
