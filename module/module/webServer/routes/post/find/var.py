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
        data: dict = await request.json()
        
        command = data.get('command')

        if command == "filter_device_id":
            device_id = data.get('device_id')
            if not device_id:
                return HTTPBadRequest(text=json.dumps({"error": str(e)}))
            else:
                vars = await MySqlConn.rawSqlCmd(f'''SELECT id, var_name, var_code, var_type, var_permission, device_id 
                                                 from vars WHERE device_id = "{device_id}" ORDER BY id ASC''')
                var_list = [{"var_id": var[0], "var_name": var[1], "var_code": var[2], "var_type": var[3], "var_permission": var[4], "device_id": var[5]} for var in vars]
                return HTTPOk(text=json.dumps(var_list))
                 
        elif command == "filter_var_id":
            var_id = data.get('var_id')
            if not var_id:
                return HTTPBadRequest(text=json.dumps({"no var_id.": str(e)}))
            else:
                vars = await MySqlConn.rawSqlCmd(f'''SELECT var_name, var_code, var_type, var_permission from vars WHERE id = "{var_id}" ORDER BY id ASC''')
                var_list = [{"var_name": var[0], "var_code": var[1], "var_type": var[2], "var_permission": var[3]} for var in vars]
                return HTTPOk(text=json.dumps(var_list))
            
        else:
            return HTTPBadRequest(text="unknow error.")
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to insert device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
    