from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router:UrlDispatcher):
    router.add_post(
        path= '/getDevice',
        handler= handle
    )

async def handle(request:Request):
    try:
        data: dict = await request.json()

        command = data.get('command')

        if command == "filter_device_id":
            device_id = data.get('device_id')
            if not device_id:
                return HTTPBadRequest(text=json.dumps({"error": str(e)}))
            else:
                device = await MySqlConn.rawSqlCmd(f'''SELECT * from devices WHERE id = "{device_id}" ORDER BY id ASC''')
                device_list = [{"device_id": ONE_device[0], "device_name": ONE_device[1], "device_num": ONE_device[2], "area_id": ONE_device[3]} for ONE_device in device]                
                return HTTPOk(text=json.dumps(device_list))
            
        elif command == "all_devices":
            devices = await MySqlConn.rawSqlCmd("SELECT id, device_name, device_num, area_id from devices ORDER BY id ASC")
            device_list = [{"device_id": device[0], "device_name": device[1], "device_num": device[2], "area_id": device[3]} for device in devices] 
            return HTTPOk(text=json.dumps(device_list))
               
        else:
            return HTTPBadRequest(text="unknow error.")
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to get device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))


        
    