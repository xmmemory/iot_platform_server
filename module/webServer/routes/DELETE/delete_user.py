from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_delete(router: UrlDispatcher):
    router.add_delete(
        path='/user',
        handler=delete_user_by_id
    )
    router.add_delete(
        path='/api/users/{id}',
        handler=api_user_del
    )
    
async def api_user_del(request: Request):
    try:
        user_id = request.match_info.get('id')

        if user_id is not None:
            res = await MySqlConn.rawSqlCmd(f'''SELECT * FROM users WHERE id = "{user_id}"''')
            print("user delete: ", res[0])
        else:
            print("user delete fail.", "user_id is none.")
            return HTTPBadRequest(text="upload data is not enough.") 
        
        res = await MySqlConn.rawSqlCmd(f'''DELETE FROM users WHERE id ="{user_id}" LIMIT 1''')
        print(res)
        return HTTPOk(text=json.dumps(res))
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))

async def delete_user_by_id(request: Request):
    try:
        data: dict = await request.json()

        user_id= data.get('user_id')        

        if user_id is not None:
            res = await MySqlConn.rawSqlCmd(f'''SELECT * FROM users WHERE id = "{user_id}"''')
            print("user delete: ", res[0])
        else:
            print("user delete fail.", "user_id is none.")
            return HTTPBadRequest(text="upload data is not enough.") 
        
        res = await MySqlConn.rawSqlCmd(f'''DELETE FROM users WHERE id ="{user_id}" LIMIT 1''')
        print(res)
        return HTTPOk(text=json.dumps(res))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
