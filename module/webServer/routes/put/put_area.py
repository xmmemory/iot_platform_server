from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_put(router: UrlDispatcher):
    router.add_put(
        path='/modify/area',
        handler=modify_area
    )

async def modify_area(request: Request):
    try:
        data: dict = await request.json()

        area_id = data.get("area_id")
        area_name = data.get("area_name")

        if area_name and area_name.strip():
            print(area_name, area_id)
        else:
            print("insufficient data.")
            return HTTPBadRequest(text="upload data is not enough.") 
                    
        res = await MySqlConn.rawSqlCmd(
                f'''UPDATE areas SET area_name = "{area_name}" WHERE id = {area_id}''')
        print(res)
        return HTTPOk(text=json.dumps(res))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
