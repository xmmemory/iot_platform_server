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
        # 从请求中获取 JSON 数据
        data = await request.json()        
        # 提取变量
        area_name = data.get("area_name")
        area_id = (await MySqlConn.rawSqlCmd(f'SELECT id FROM areas WHERE area_name = "{area_name}"'))
        if not area_id:
            data = await MySqlConn.rawSqlCmd(f'INSERT INTO areas (area_name) VALUES ("{area_name}")')
            print(data)
            # 返回成功消息
            return HTTPOk(text="分区添加成功")
        else:
            return HTTPBadRequest(text="添加失败，分区已存在")
        # await y_async_db.execute_query(f"INSERT INTO devices (device_name, device_num, area_id) VALUES (%s, %s, %s)", (device_name, device_num, area_id))

    except ValueError as ve:
        # 捕获缺失字段错误
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        # 捕获其他所有错误
        print(f"Failed to insert device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
