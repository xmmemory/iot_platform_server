from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_delete(router: UrlDispatcher):
    router.add_delete(
        path='/area/id/f',
        handler=delete_area_by_id
    )

async def delete_area_by_id(request: Request):
    try:
        data: dict = await request.json()

        area_id= data.get('area_id')

        if area_id is not None:
            result = await MySqlConn.rawSqlCmd(f'''SELECT * FROM areas WHERE id = "{area_id}"''')
            if not result:
                return HTTPBadRequest(text="No record found for deletion.")
            else:
                res = await MySqlConn.rawSqlCmd(f'''DELETE FROM areas WHERE id ="{area_id}" LIMIT 1''')
                return HTTPOk(text=json.dumps(res))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
