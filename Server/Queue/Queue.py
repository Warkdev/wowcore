import asyncio


class Queue(object):

    def __init__(self, loop, maxsize: int):
        self.instance = asyncio.Queue(loop = loop, maxsize = maxsize)

    async def put(self, data):
        await self.instance.put(data)

    async def get(self):
        data = await self.instance.get()
        self.instance.task_done()
        return data

    @staticmethod
    def get_instance():
        return Queue(loop = asyncio.get_event_loop(), maxsize = 10)


queue = Queue.get_instance()
