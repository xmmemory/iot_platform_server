from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/modifyVar',
        handler=modify
    )
async def modify(request: Request):
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

    # 提取变量
    var_name = data.get("var_name")
    var_code = data.get("var_code")
    var_type = data.get("var_type")
    var_permission = data.get("var_permission")
    device_id = data.get("device_id")
    var_id = data.get("var_id")

    if command == "insert_var":
        print("insert_var")
        data = await MySqlConn.rawSqlCmd(
            f'''INSERT INTO vars (var_name, var_code, var_type, var_permission, device_id)
              VALUES ("{var_name}","{var_code}", "{var_type}", "{var_permission}", {device_id})''')
        print(data)
        # 返回成功消息
        return HTTPOk(text=json.dumps(data))
        
    elif command == "update_var":
        print("update_var")
        data = await MySqlConn.rawSqlCmd(
                f'''UPDATE vars SET
                var_name = "{var_name}",
                var_code = "{var_code}",
                var_type = "{var_type}",
                var_permission = "{var_permission}",
                device_id = "{device_id}"
                WHERE id = {var_id}''')
        print(data)
        # 返回成功消息
        return HTTPOk(text=json.dumps(data))
    