from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json
from module.db.db_async import y_async_db

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/insertDevice',
        handler=insert
    )

async def insert(request: Request):
    try:
        # 从请求中获取 JSON 数据
        data = await request.json()
        print(data)  # 打印接收到的数据，便于调试
        
        # 提取变量
        device_name = data.get("device_name")
        device_num = data.get("device_num")
        area_id = data.get("area_id")

        # # 检查必要的字段是否都存在
        # if not device_name or not device_num or not area_id:
        #     raise ValueError("Missing required fields: 'name', 'num', or 'area_id'")

        # # SQL 插入语句
        # insert_query = """
        # INSERT INTO devices (device_name, device_num, area_id)
        # VALUES (%s, %s, %s)
        # """
        # values = (device_name, device_num, area_id)

        # # 获取数据库连接和游标 (假设你已经有 MySQL 连接管理器)
        # async with MySqlConn.get_cursor() as cursor:  # 获取异步游标
        #     # 执行插入操作
        #     await MySqlConn.rawSqlCmd(cursor, insert_query, values)

        await y_async_db.execute_query(f"INSERT INTO devices (device_name, device_num, area_id) VALUES (%s, %s, %s)", (device_name, device_num, area_id))

        # 返回成功消息
        return HTTPOk(text=json.dumps({"message": "Device data inserted successfully."}))

    except ValueError as ve:
        # 捕获缺失字段错误
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        # 捕获其他所有错误
        print(f"Failed to insert device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
