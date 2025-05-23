from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/users',
        handler= get_all_users
    )
    router.add_get(
        path= '/user/info/f',
        handler= get_user_info
    )
    # api
    router.add_get(
        path= '/api/users',
        handler= api_get_users
    )

async def api_get_users(request:Request):
    users = await MySqlConn.rawSqlCmd("SELECT id, name, permission from users ORDER BY id ASC")
    user_list = [{"id": user[0], "username": user[1], "role": user[2]} for user in users]
    # 将 user_list 包装在 data 字段中
    response_data = {
        "data": user_list
    }
    
    # 返回 JSON 响应
    return HTTPOk(text=json.dumps(response_data), content_type="application/json")

async def get_all_users(request:Request):
    users = await MySqlConn.rawSqlCmd("SELECT id, name, permission from users ORDER BY id ASC")
    user_list = [{"id": user[0], "name": user[1], "permission": user[2]} for user in users]
    return HTTPOk(text=json.dumps(user_list))

async def get_user_info(request:Request):
    try:
        # 从 GET 请求中获取 'username' 参数
        username = request.query.get('username')  # 从查询参数中获取字段

        if username and username.strip():
            vars = await MySqlConn.rawSqlCmd(f'''SELECT permission, latest_version from users WHERE name = "{username}" ORDER BY id ASC''')
            var_list = [{"permission": info[0], "latest_version": info[1]} for info in vars]
            return HTTPOk(text=json.dumps(var_list))
            
        else:
            return HTTPBadRequest(text="unknow error.")
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to get device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
