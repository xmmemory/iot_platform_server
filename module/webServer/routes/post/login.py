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
    permission = 'user'

    try:
        # 查询用户 ID 和密码
        user_data = await MySqlConn.rawSqlCmd(f'SELECT id, password, permission FROM users WHERE name = "{entered_user}"')
        user_id, hashed_password, permission = user_data[0]
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

         # 获取用户 IP 地址
        ip_address = request.remote or "Unknown"
        # 获取 User-Agent（设备信息）
        device_info = request.headers.get("User-Agent", "Unknown")
        # 记录登录操作到 user_activity_logs
        query = f'''
        INSERT INTO user_activity_logs (user_id, action_type, action_time, ip_address, device_info, description, local_version)
        VALUES ({user_id}, "登录", NOW(), "{ip_address}", "{device_info}", "token={token}", "{local_version}")
        '''
        await MySqlConn.rawSqlCmd(query)
        
        res = [{"token": token, "permission": permission}]
        return HTTPOk(text=json.dumps(res))
    else:
        return HTTPUnauthorized(text="密码错误")
