from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/controlVar',
        handler=control
    )
async def control(request: Request):
    try:
        data: dict = await request.json()
    
        command = data.get('command')

        var_name = data.get("var_name")
        var_code = data.get("var_code")
        var_type = data.get("var_type")
        var_permission = data.get("var_permission")
        device_id = data.get("device_id")
        var_id = data.get("var_id")

        if command == "del_var" and var_id is not None:
            result = await MySqlConn.rawSqlCmd(f'''SELECT * FROM vars WHERE id = "{var_id}"''')
            if not result:
                return HTTPBadRequest(text="No record found for deletion.")
            else:
                res = await MySqlConn.rawSqlCmd(f'''DELETE FROM vars WHERE id ="{var_id}" LIMIT 1''')
                return HTTPOk(text=json.dumps(res))

        if (var_name and var_name.strip() and var_code is not None and var_type and var_type.strip() and var_permission and var_permission.strip() and device_id is not None):
            print(command, var_name, var_code, var_type, var_permission, device_id, var_id)
        else:
            print(command, "insufficient data:", var_name, var_code, var_type, var_permission, device_id, var_id)
            return HTTPBadRequest(text="upload data is not enough.") 

        if command == "onOff":
            # TODO 应该在插入数据之前，首先判断是否存在相同设备(var_code & device_id相同)
            if 1:   
                data = await MySqlConn.rawSqlCmd(
                    f'''INSERT INTO vars (var_name, var_code, var_type, var_permission, device_id)
                    VALUES ("{var_name}","{var_code}", "{var_type}", "{var_permission}", {device_id})''')
                print(data)
                return HTTPOk(text=json.dumps(data))
            else:
                return HTTPBadRequest(text="insert device fail, var is exist.")  
            
        elif command == "update_var":
            data = await MySqlConn.rawSqlCmd(
                    f'''UPDATE vars SET
                    var_name = "{var_name}",
                    var_code = "{var_code}",
                    var_type = "{var_type}",
                    var_permission = "{var_permission}",
                    device_id = "{device_id}"
                    WHERE id = {var_id}''')
            print(data)
            return HTTPOk(text=json.dumps(data))
                
        else:
            return HTTPBadRequest(text="unknow error.")
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to insert vars data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
    