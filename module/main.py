import sys
sys.dont_write_bytecode = True


import signal
from asyncio import Event
shutdown_event = Event()
def handle_sigint(signal, frame):
    print("\nSIGINT received! Graceful shutdown...\n")
    shutdown_event.set()
signal.signal(signal.SIGINT, handle_sigint)


import asyncio
from module.webServer import WebServer
# 
from module.db.db_async import init_db, close_db

HOST = "0.0.0.0"
PORT = 9013

async def main():
    # 初始化数据库连接
    await init_db()

    server = WebServer(HOST, PORT)
    asyncio.create_task(server.start())

    await shutdown_event.wait()
    await server.shutdown()

    # 关闭数据库连接池
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())
