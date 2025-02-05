import asyncio
import aiohttp.web
import ssl
import sys

from module.db.mysqlConn import MySqlConn
from . import routes
from module.mqtt.subscriber import MqttSubscriber

class WebServer:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        self.app = aiohttp.web.Application()

        if '--https' in sys.argv:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_context.load_cert_chain(
                certfile='./certs/fullchain.pem',
                keyfile='./certs/privkey.pem'
            )

        self.setup_routes()
        self.stop_event = asyncio.Event()


    def setup_routes(self):
        routes.add_routes(self.app.router)
        self.app.router.add_static("/download", "./file",show_index=True)
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
        # mysql数据库
        await MySqlConn.openConn("101.201.60.179", 3306, "lrl", "Asynchronous_20241219", "lvrulan_mysql")
        MySqlConn.useDb("lvrulan_mysql")
        print(f"\033[1;32mWeb server started.")
        print(f"\033[1;30m", end='')
        print(f"  -- host:    {self.host}")
        print(f"  -- port:    {self.port}")
        print(f"  -- proc:    {'https' if '--https' in sys.argv else 'http'}")
        print("\033[0m")
        # mqtt
        mqtt = MqttSubscriber().connect("101.201.60.179", 1883, "lrl001", "123456")
        mqtt.subscribe("40800965")
        self.mqtt_task = asyncio.get_running_loop().create_task(mqtt.listen())

    async def shutdown(self):
        self.stop_event.set()
        await self.site.stop()
        await self.runner.cleanup()
        print("self.mqtt_task.cancel...")
        self.mqtt_task.cancel()
        print("self.mqtt_task.cancel---finish.")
        await MySqlConn.closeConn('lvrulan_mysql')
        print("\033[1;33mWeb server shutting down.")
        print("\033[0m")
