from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router:UrlDispatcher):
    router.add_post(
        path= '/getVar',
        handler= handle
    )

async def handle(request:Request):
    try:
        # 获取 JSON 数据
        data: dict = await request.json()
    except ValueError as ve:
        # 捕获缺失字段错误
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        # 捕获其他所有错误
        print(f"Failed to insert device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
        
    command = data.get('command')

    if command == "filter_device_id":
        device_id = data.get('device_id')
        if not device_id:
            return HTTPBadRequest(text=json.dumps({"error": str(e)}))
        else:
            vars = await MySqlConn.rawSqlCmd(f'''SELECT * from vars WHERE device_id = "{device_id}" ORDER BY id ASC''')
            print(vars)
            return HTTPOk(text=json.dumps(vars))
    
    elif command == "filter_var_id":
        var_id = data.get('var_id')
        if not var_id:
            return HTTPBadRequest(text=json.dumps({"error": str(e)}))
        else:
            res = await MySqlConn.rawSqlCmd(f'''SELECT * from vars WHERE id = "{var_id}" ORDER BY id ASC''')
            print(res)
            return HTTPOk(text=json.dumps(res))

    # vars = await MySqlConn.rawSqlCmd("SELECT id, var_name, var_code, var_type, var_permission from vars ORDER BY id ASC")
    
    