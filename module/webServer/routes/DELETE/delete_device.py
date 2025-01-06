from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_delete(router: UrlDispatcher):
    router.add_delete(
        path='/device/id/f',
        handler=delete_device_by_id
    )

async def delete_device_by_id(request: Request):
    try:
        data: dict = await request.json()

        device_id= data.get('device_id')

        if device_id is not None:
            result = await MySqlConn.rawSqlCmd(f'''SELECT * FROM devices WHERE id = "{device_id}"''')
            if not result:
                return HTTPBadRequest(text="No record found for deletion.")
            else:
                res = await MySqlConn.rawSqlCmd(f'''DELETE FROM devices WHERE id ="{device_id}" LIMIT 1''')
                return HTTPOk(text=json.dumps(res))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
