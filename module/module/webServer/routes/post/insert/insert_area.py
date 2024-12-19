from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/insertArea',
        handler=insert
    )

async def insert(request: Request):
    try:
        data = await request.json()   
        area_name = data.get("area_name")
        area_id = (await MySqlConn.rawSqlCmd(f'SELECT id FROM areas WHERE area_name = "{area_name}"'))
        if not area_id:
            data = await MySqlConn.rawSqlCmd(f'INSERT INTO areas (area_name) VALUES ("{area_name}")')
            print(data)
            return HTTPOk(text="分区添加成功")
        else:
            return HTTPBadRequest(text="添加失败，分区已存在")

    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to insert device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
