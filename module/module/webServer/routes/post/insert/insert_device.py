from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

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

        device_id = (await MySqlConn.rawSqlCmd
                     (f'''SELECT id FROM devices 
                      WHERE device_name = "{device_name}" AND device_num = "{device_num}" AND area_id = "{area_id}"'''))

        if not device_id:
            data = await MySqlConn.rawSqlCmd(
            f'INSERT INTO devices (device_name, device_num, area_id) VALUES ("{device_name}",{device_num}, {area_id})')
            print(data)
            # 返回成功消息
            return HTTPOk(text="设备添加成功")
        else:
            return HTTPBadRequest(text="添加失败，设备已存在")            
        # await y_async_db.execute_query(f"INSERT INTO devices (device_name, device_num, area_id) VALUES (%s, %s, %s)", (device_name, device_num, area_id))

    except ValueError as ve:
        # 捕获缺失字段错误
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        # 捕获其他所有错误
        print(f"Failed to insert device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
