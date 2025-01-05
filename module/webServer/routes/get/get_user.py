from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/users',
        handler= get_all_users
    )

async def get_all_users(request:Request):
    users = await MySqlConn.rawSqlCmd("SELECT id, username, permission from users ORDER BY id ASC")
    user_list = [{"id": user[0], "name": user[1], "permission": user[2]} for user in users]
    return HTTPOk(text=json.dumps(user_list))
