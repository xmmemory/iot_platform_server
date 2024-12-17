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
        print(data)
        return HTTPBadRequest(text=f"Invalid request format. {e}")
    
    print(data)

    username = data.get('username')
    password = data.get('password')

    try:
        # 直接从数据库获取密码
        user_password = (await MySqlConn.rawSqlCmd(f'SELECT password FROM users WHERE username = "{username}"'))[0][0]
    except IndexError:
        return HTTPUnauthorized(reason="Invalid username")
    
    # 直接比较明文密码
    if user_password == password:
        # 生成唯一的 token
        token = secrets.token_hex(16)
        await MySqlConn.rawSqlCmd(f'UPDATE users SET token = "{token}" WHERE username = "{username}"')

        # await y_async_db.connect()  # 你可以调用 db 连接池的 connect 方法来确保连接
        # await y_async_db.execute_query(f"INSERT INTO devices (device_name, device_num, area_id) VALUES (%s, %s, %s)", ("氨气传感器", 2, 2))
        # await y_async_db.close()  # 完成后关闭连接池

        return HTTPOk(text=f"authorized-token={token}")
    
    else:
        return HTTPUnauthorized(text="账户名或密码错误")