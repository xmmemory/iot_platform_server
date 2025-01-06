from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_put(router: UrlDispatcher):
    router.add_put(
        path='/modify/device',
        handler=var_setting
    )

async def var_setting(request: Request):
    try:
        data: dict = await request.json()

        device_id = data.get("device_id")
        device_name = data.get("device_name")
        device_num = data.get("device_num")
        area_id = data.get("area_id")
        icon_addr = data.get("icon_addr")
    
        if device_name and device_name.strip() and area_id is not None:
            print(device_name, device_num, area_id, device_id, icon_addr)
        else:
            print("insufficient data:", device_name, device_num, area_id, device_id, icon_addr)
            return HTTPBadRequest(text="upload data is not enough.") 
        
        res = await MySqlConn.rawSqlCmd(
                f'''UPDATE devices SET device_name = "{device_name}", device_num = "{device_num}", area_id = "{area_id}", icon_addr= "{icon_addr}" WHERE id = {device_id}''')
        print(res)            
        return HTTPOk(text=json.dumps(res))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))