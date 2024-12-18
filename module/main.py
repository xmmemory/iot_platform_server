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

HOST = "0.0.0.0"
PORT = 9013

async def main():

    server = WebServer(HOST, PORT)
    asyncio.create_task(server.start())

    await shutdown_event.wait()
    await server.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
