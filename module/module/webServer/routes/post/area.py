from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router:UrlDispatcher):
    router.add_post(
        path= '/getArea',
        handler= handle
    )

async def handle(request:Request):       
    device = await MySqlConn.rawSqlCmd("SELECT id, area_name from areas")   
    return HTTPOk(text=json.dumps(device))