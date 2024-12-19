from aiohttp import web
import secrets  # 用于生成随机 token
from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest, HTTPUnauthorized
from module.db.mysqlConn import MySqlConn

def add_post(router: UrlDispatcher):
    router.add_post('/login', handler=login)

async def login(request: Request):
    try:
        # 获取 JSON 数据
        data: dict = await request.json()
    except Exception as e:
        return HTTPBadRequest(text=f"Invalid request format. {e}")
    
    username = data.get('username')
    password = data.get('password')

    try:
        # 直接从数据库获取密码
        user_password = (await MySqlConn.rawSqlCmd(f'SELECT password FROM users WHERE username = "{username}"'))
        user_password = user_password[0][0]
    except IndexError:
        return HTTPUnauthorized(reason="用户不存在")
    
    # 直接比较明文密码
    if user_password == password:
        # 生成唯一的 token
        token = secrets.token_hex(16)
        print(token, type(token))
        await MySqlConn.rawSqlCmd(f'UPDATE users SET token = "{token}" WHERE username = "{username}"')
        return HTTPOk(text=f"authorized-token={token}")
    else:
        return HTTPUnauthorized(text="密码错误")