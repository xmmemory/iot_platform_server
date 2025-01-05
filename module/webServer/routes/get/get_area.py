from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/areas',
        handler= get_all_areas
    )

async def get_all_areas(request:Request):
    areas = await MySqlConn.rawSqlCmd("SELECT id, area_name from areas ORDER BY id ASC")
    area_list = [{"area_id": area[0], "area_name": area[1]} for area in areas]
    return HTTPOk(text=json.dumps(area_list))
