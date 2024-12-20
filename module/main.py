import sys
sys.dont_write_bytecode = True # try not to generate "__pycache__" folders


from asyncio import Event
shutdown_event = Event()

from module.webServer import WebServer
HOST = "0.0.0.0"
PORT = 7500
async def main():

    server = WebServer(HOST, PORT)
    asyncio.create_task(server.start())

    await shutdown_event.wait()
    await server.shutdown()


import asyncio
import signal
import os # os.name equals 'nt' for Windows, 'posix' for Unix/Linux
if os.name == 'nt':
    def handle_sigint(signal, frame):
        print("\nSIGINT received!\nGraceful shutdowning, please wait for the program closed patiently...\n")
        shutdown_event.set()
    signal.signal(signal.SIGINT, handle_sigint)
    asyncio.run(main())
elif os.name == 'posix':
    def handle_sigint():
        print("\nSIGINT received!\nGraceful shutdowning, please wait for the program closed patiently...\n")
        shutdown_event.set()
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, handle_sigint)
    try:
        loop.run_until_complete(main())
    except asyncio.CancelledError: ...
    finally:
        loop.close()