from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/user',
        handler= handle_all_user
    )

async def handle_all_user(request:Request):
    users = await MySqlConn.rawSqlCmd("SELECT id, username, permission from users ORDER BY id ASC")
    user_list = [{"id": user[0], "name": user[1], "permission": user[2]} for user in users]
    return HTTPOk(text=json.dumps(user_list))
