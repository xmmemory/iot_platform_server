from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/modifyArea',
        handler=modify
    )

async def modify(request: Request):
    try:
        data: dict = await request.json()

        command = data.get('command')

        area_id = data.get("area_id")
        area_name = data.get("area_name")

        if command == "del_area" and area_id is not None:
            result = await MySqlConn.rawSqlCmd(f'''SELECT * FROM areas WHERE id = "{area_id}"''')
            if not result:
                return HTTPBadRequest(text="No record found for deletion.")
            else:
                res = await MySqlConn.rawSqlCmd(f'''DELETE FROM areas WHERE id ="{area_id}" LIMIT 1''')
                return HTTPOk(text=json.dumps(res))

        if area_name and area_name.strip():
            print(command, area_name, area_id)
        else:
            print(command, "insufficient data.")
            return HTTPBadRequest(text="upload data is not enough.") 

        if command == "insert_area":
            # TODO 应该在插入数据之前，首先判断是否存在相同设备
            if 1:             
                res = await MySqlConn.rawSqlCmd(
                f'INSERT INTO areas (area_name) VALUES ("{area_name}")')
                print(res)
                return HTTPOk(text=json.dumps(res))
            else:
                return HTTPBadRequest(text="insert area fail, area is exist.")        
                    
        elif command == "update_area":
            res = await MySqlConn.rawSqlCmd(
                    f'''UPDATE areas SET area_name = "{area_name}" WHERE id = {area_id}''')
            print(res)
            return HTTPOk(text=json.dumps(res))
                    
        else:
            return HTTPBadRequest(text="unknow error.")
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
