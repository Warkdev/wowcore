from Server.LoginServer import LoginServer
from Server.WorldServer import WorldServer
import asyncio


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    login_server = LoginServer.create()
    world_server = WorldServer.create()

    loop.run_until_complete(
        asyncio.gather(
            login_server.get_instance(),
            world_server.get_instance()
        )
    )

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()
