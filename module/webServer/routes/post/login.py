from aiohttp import web
import secrets  # 用于生成随机 token
from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest, HTTPUnauthorized
from module.db.mysqlConn import MySqlConn
import bcrypt # type: ignore
import json

def add_post(router: UrlDispatcher):
    router.add_post('/login', handler=login)

async def login(request: Request):
    try:
        # 获取 JSON 数据
        data: dict = await request.json()
    except Exception as e:
        return HTTPBadRequest(text=f"Invalid request format. {e}")
    
    entered_user = data.get('username')
    entered_password = data.get('password')
    local_version = data.get('local_version')

    try:
        # 直接从数据库获取密码
        user_password = (await MySqlConn.rawSqlCmd(f'SELECT password FROM users WHERE name = "{entered_user}"'))
        hashed_password = user_password[0][0]        
        del user_password
    except IndexError:
        return HTTPUnauthorized(reason="用户不存在")
    
    auth_pass = False

    try:    
        if bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8')):
            auth_pass = True
    except ValueError:
        pass

    print("login, user: ", entered_user)
    
    # 直接比较明文密码
    if entered_password == hashed_password:
        auth_pass = True
    
    if auth_pass:
        # 生成唯一的 token
        token = secrets.token_hex(16)
        print(token, type(token))
        await MySqlConn.rawSqlCmd(f'UPDATE users SET token = "{token}", local_version = "{local_version}" WHERE name = "{entered_user}"')
        
        # 记录登录操作
        table_name = f"user_{entered_user}"
        await MySqlConn.insertOperation(table_name, "登录", f"token={token}")
        
        return HTTPOk(text=f"authorized-token={token}")
    else:
        return HTTPUnauthorized(text="密码错误")
