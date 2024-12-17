import asyncio
import aiohttp.web
import ssl
import sys


from module.db.mysqlConn import MySqlConn
from . import routes


class WebServer:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.app = aiohttp.web.Application()
        self.mysqlDb = MySqlConn("127.0.0.1", 3306, "root", "FORever1437", "lvrulan_mysql")

        if '--https' in sys.argv:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(
                certfile='/etc/letsencrypt/live/ynufe.tech/fullchain.pem',
                keyfile='/etc/letsencrypt/live/ynufe.tech/privkey.pem'
            )

        self.setup_routes()
        self.stop_event = asyncio.Event()


    def setup_routes(self):
        routes.add_routes(self.app.router)

        async def handle_404(request:aiohttp.web.Request):
            return aiohttp.web.HTTPNotFound(text=f"404 Not Found:\n{request.path}")
        self.app.router.add_route('*', '/{tail:.*}', handle_404)


    async def start(self):
        self.runner = aiohttp.web.AppRunner(self.app)
        await self.runner.setup()
        self.site = aiohttp.web.TCPSite(
            runner= self.runner,
            host= self.host,
            port= self.port,
            ssl_context= self.ssl_context if '--https' in sys.argv else None
        )
        await self.site.start()
        await self.mysqlDb.openConn()
        print(f"\033[1;32mWeb server started.")
        print(f"\033[1;30m", end='')
        print(f"  -- host:    {self.host}")
        print(f"  -- port:    {self.port}")
        print(f"  -- proc:    {'https' if '--https' in sys.argv else 'http'}")
        print("\033[0m")
        await self.stop_event.wait()


    async def shutdown(self):
        self.stop_event.set()
        await self.site.stop()
        await self.runner.cleanup()
        await self.mysqlDb.closeConn()
        print("\033[1;33mWeb server shutting down.")
        print("\033[0m")