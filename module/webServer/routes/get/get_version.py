from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/version/f',
        handler= get_version_by_username
    )

async def get_version_by_username(request:Request):
    try:
        # 从 GET 请求中获取 'username' 参数
        username = request.query.get('username')  # 从查询参数中获取字段

        if username and username.strip():
            version = await MySqlConn.rawSqlCmd(f'''SELECT latest_version from users WHERE name = "{username}" ORDER BY id ASC''')
            # 将version转换为JSON格式并返回HTTPOk响应
            return HTTPOk(text=json.dumps({"latest_version": version}))
            
        else:
            return HTTPBadRequest(text="unknow error.")
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to get device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))