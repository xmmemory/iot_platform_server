import asyncio
from aiohttp import web
import ssl
import sys

from module.db.mysqlConn import MySqlConn
from . import routes
from module.mqtt.subscriber import MqttSubscriber

class WebServer:
    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port
        # self.app = web.Application()
        self.app = web.Application(middlewares=[self.auth_middleware])

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
        async def handle_404(request:web.Request):
            return web.HTTPNotFound(text=f"404 Not Found:\n{request.path}")
        self.app.router.add_route('*', '/{tail:.*}', handle_404)

    async def auth_middleware(self, app, handler):
        async def middleware_handler(request):
            # 允许登录接口和静态文件路径绕过验证
            if request.path in ["/login", "/download"] or request.path.startswith("/static/"):
                return await handler(request)
            
            token = request.headers.get("Authorization", "").replace("Bearer ", "")
            if not token:
                print("Missing token")
                return web.HTTPUnauthorized(text="Missing token")

            user = await MySqlConn.rawSqlCmd(f"SELECT id FROM users WHERE token = '{token}'")
            if not user:
                print("Invalid token")
                return web.HTTPUnauthorized(text="Invalid token")
            
            print(f"User {user[0][0]} authorized")
            request["user_id"] = user[0][0]  # 存入请求，后续可用
            return await handler(request)

        return middleware_handler


    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(
            runner= self.runner,
            host= self.host,
            port= self.port,
            ssl_context= self.ssl_context if '--https' in sys.argv else None
        )
        await self.site.start()
        # mysql数据库
        await MySqlConn.openConn(
            host="101.201.60.179", 
            port=3306, 
            user="lrl", 
            password="Asynchronous_20241219", 
            db_name="lvrulan_mysql"  # 这里是数据库名
        )

        # await MySqlConn.openConn("101.201.60.179", 3306, "lrl", "Asynchronous_20241219", "lvrulan_mysql")
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

        # 启动定时任务
        asyncio.create_task(self.periodic_update_device_status())

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

    async def update_vars_status(self):
        query = """
        UPDATE device_variables
        SET status = 'ABNORMAL', updated_at = updated_at
        WHERE status = 'NORMAL' 
        AND TIMESTAMPDIFF(SECOND, updated_at, NOW()) > 60;
        """
        await MySqlConn.execute(query)
        # print("Updated var status to ABNORMAL for devices that have not been updated in the last 60 seconds.")

    async def restore_vars_status(self):
        query = """
        UPDATE device_variables
        SET status = 'NORMAL', updated_at = updated_at
        WHERE status = 'ABNORMAL' 
        AND TIMESTAMPDIFF(SECOND, updated_at, NOW()) <= 60;
        """
        await MySqlConn.execute(query)
        # print("Restored var status to NORMAL for devices that have been updated in the last 60 seconds.")

    async def update_device_status(self):
        query = """
        UPDATE devices d
        SET d.status = 'ABNORMAL'
        WHERE d.id IN (
            SELECT DISTINCT dv.device_id
            FROM device_variables dv
            WHERE dv.status = 'ABNORMAL'
        );
        """
        await MySqlConn.execute(query)
        # print("Restored device status to NORMAL for devices that have been updated in the last 60 seconds.")

    async def restore_device_status(self):
        query = """
        UPDATE devices d
        SET d.status = 'NORMAL'
        WHERE d.id IN (
            SELECT dv.device_id
            FROM device_variables dv
            GROUP BY dv.device_id
            HAVING SUM(CASE WHEN dv.status = 'ABNORMAL' THEN 1 ELSE 0 END) = 0
        );
        """
        await MySqlConn.execute(query)
        # print("Restored device status to NORMAL for devices that have been updated in the last 60 seconds.")

    async def periodic_update_device_status(self):
        while not self.stop_event.is_set():
            await self.update_vars_status()
            await asyncio.sleep(5)
            await self.restore_vars_status()
            await asyncio.sleep(5)
            await self.update_device_status()
            await asyncio.sleep(5)
            await self.restore_device_status()
            await asyncio.sleep(45)  # 每隔 60 秒执行一次

