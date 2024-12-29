from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/var/id/f',
        handler= filter_var_id
    )
    router.add_get(
        path= '/var/record/f',
        handler= handle_device_var
    )
    router.add_get(
        path= '/var/device/f',
        handler= filter_device_id
    )
    

async def filter_var_id(request:Request):
    try:
        # 从 GET 请求中获取 'device_id' 参数
        var_id = request.query.get('var_id')  # 从查询参数中获取字段 
        if not var_id:
            return HTTPBadRequest(text=json.dumps({"no var_id.": str(e)}))
        else:
            vars = await MySqlConn.rawSqlCmd(f'''SELECT var_name, var_code, var_type, var_permission from vars WHERE id = "{var_id}" ORDER BY id ASC''')
            var_list = [{"var_name": var[0], "var_code": var[1], "var_type": var[2], "var_permission": var[3]} for var in vars]
            return HTTPOk(text=json.dumps(var_list))
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify var data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))

  
async def handle_device_var(request:Request):
    try:
        # 从 GET 请求中获取 'device_id' 参数
        full_code = request.query.get('full_code')  # 从查询参数中获取字段 
        
        # 用下划线替换点号，避免表名错误
        table_name = f"var_{full_code.replace('.', '_')}"

        vars = await MySqlConn.rawSqlCmd(f'''SELECT value, created_at from `{table_name}` ORDER BY id DESC LIMIT 20''')
        # print(vars)
        var_list = [{"value": var[0], "created_at": var[1]} for var in vars]
        # print(var_list)
        # 转换 datetime 为字符串
        for item in var_list:
            item['created_at'] = item['created_at'].isoformat()
        return HTTPOk(text=json.dumps(var_list))
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify var data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
    
async def filter_device_id(request:Request):
    try:
        # 从 GET 请求中获取 'device_id' 参数
        device_id = request.query.get('device_id')  # 从查询参数中获取字段        

        if not device_id:
            return HTTPBadRequest(text=json.dumps({"error"}))
        else:
            vars = await MySqlConn.rawSqlCmd(f'''SELECT id, var_name, var_code, var_type, var_permission, latest_value, last_datetime, var_full_code 
                                                 from vars WHERE device_id = "{device_id}" ORDER BY id ASC''')
            var_list = [{"var_id": var[0], "var_name": var[1], "var_code": var[2], "var_type": var[3], "var_permission": var[4],
                            "latest_value": var[5], "last_datetime": var[6], "var_full_code": var[7] } for var in vars]
            
            # print(var_list)
            for item in var_list:
                if item['last_datetime']:
                    item['last_datetime'] = item['last_datetime'].isoformat()
                else:
                    # 处理为空的情况，比如设置为默认值
                    item['last_datetime'] = 'N/A'  # 或者其他你希望的默认值
            # print(var_list)
            return HTTPOk(text=json.dumps(var_list))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)})) 

    except Exception as e:
        print(f"Failed to get device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))