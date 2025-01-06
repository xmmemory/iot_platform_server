from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/user',
        handler=add_user
    )

async def add_user(request: Request):
    try:
        data: dict = await request.json()

        user_name = data.get('user_name')
        user_password = data.get("user_password")

        if user_name and user_name.strip() and user_password and user_password.strip():
            print("user add, name: ", user_name, "ps: " , user_password)
        else:
            print("user add fail.", "insufficient data.")
            return HTTPBadRequest(text="upload data is not enough.") 

        res = await MySqlConn.rawSqlCmd(f'''SELECT * FROM users WHERE username = "{user_name}"''')
        if not res:
            res = await MySqlConn.rawSqlCmd(
            f'INSERT INTO users (username, password) VALUES ("{user_name}", "{user_password}")')
            print(res)
            return HTTPOk(text=json.dumps(res))
        else:
            return HTTPBadRequest(text="insert user fail, user is exist.")  
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
