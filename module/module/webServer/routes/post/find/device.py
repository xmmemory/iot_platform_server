from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router:UrlDispatcher):
    router.add_post(
        path= '/getDevice',
        handler= handle
    )

async def handle(request:Request):
    device = await MySqlConn.rawSqlCmd("SELECT id, device_name, device_num, area_id from devices ORDER BY id ASC")   
    return HTTPOk(text=json.dumps(device))