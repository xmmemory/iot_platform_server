from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router:UrlDispatcher):
    router.add_post(
        path= '/getVersion',
        handler= handle
    )

async def handle(request:Request):
    try:
        data: dict = await request.json()

        username = data.get('username')

        if username and username.strip():
            version = await MySqlConn.rawSqlCmd(f'''SELECT latest_version from users WHERE username = "{username}" ORDER BY id ASC''')
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