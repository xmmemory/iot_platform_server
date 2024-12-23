from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
from datetime import datetime
import json

def add_post(router:UrlDispatcher):
    router.add_post(
        path= '/getVarValue',
        handler= handle
    )

async def handle(request:Request):
    try:
        data: dict = await request.json()
        
        command = data.get('command')
        var_full_code = data.get('var_full_code')

        # 用下划线替换点号，避免表名错误
        table_name = f"var_{var_full_code.replace('.', '_')}"

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
    