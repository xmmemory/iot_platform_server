from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
from .models import AddUserRequest
from pydantic import ValidationError # type: ignore
import bcrypt # type: ignore
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/user',
        handler=add_user
    )
    # api
    router.add_post(
        path='/api/users',
        handler=api_users
    )

async def api_users(request: Request):
    try:
        data = await request.json()

        username = data.get('username')
        password = data.get('password')

        print("user add, name: ", username, "ps: " , password)

        # 对密码进行哈希处理
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        index = await MySqlConn.rawSqlCmd(f'''SELECT * FROM users WHERE name = "{username}"''')
        if not index:
            res = await MySqlConn.rawSqlCmd(
            f'INSERT INTO users (name, password, permission) VALUES ("{username}", "{hashed_password.decode("utf-8")}", "visitor")')
            print(res)
            
            # 创建用户操作记录表
            table_name = f"user_{username}"
            if await MySqlConn.createTable(table_name):
                return HTTPOk(text=json.dumps(res))
            else:
                return HTTPBadRequest(text="User created but failed to create operation log table")
        else:
            return HTTPBadRequest(text="insert user fail, user is exist.")

    except ValidationError as e:
        return HTTPBadRequest(text=json.dumps({"errors": e.errors()}))

async def add_user(request: Request):
    try:
        data = await request.json()
        user_data = AddUserRequest(**data)

        print("user add, name: ", user_data.user_name, "ps: " , user_data.user_password)

        # 对密码进行哈希处理
        hashed_password = bcrypt.hashpw(user_data.user_password.encode('utf-8'), bcrypt.gensalt())

        index = await MySqlConn.rawSqlCmd(f'''SELECT * FROM users WHERE name = "{user_data.user_name}"''')
        if not index:
            res = await MySqlConn.rawSqlCmd(
            f'INSERT INTO users (name, password) VALUES ("{user_data.user_name}", "{hashed_password.decode("utf-8")}")')
            print(res)
            
            # 创建用户操作记录表
            table_name = f"user_{user_data.user_name}"
            if await MySqlConn.createTable(table_name):
                return HTTPOk(text=json.dumps(res))
            else:
                return HTTPBadRequest(text="User created but failed to create operation log table")
        else:
            return HTTPBadRequest(text="insert user fail, user is exist.")

    except ValidationError as e:
        return HTTPBadRequest(text=json.dumps({"errors": e.errors()}))
