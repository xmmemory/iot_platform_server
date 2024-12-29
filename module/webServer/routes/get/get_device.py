from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/device',
        handler= handle_all_devices
    )
    router.add_get(
        path= '/device/f',
        handler= device_detail_filter_by_id
    )

async def handle_all_devices(request:Request):
    devices = await MySqlConn.rawSqlCmd("SELECT id, device_name, device_num, area_id, icon_addr from devices ORDER BY id ASC")
    device_list = [{"device_id": device[0], "device_name": device[1], 
                    "device_num": device[2], "area_id": device[3], "icon_addr": device[4]} for device in devices] 
    return HTTPOk(text=json.dumps(device_list))

async def device_detail_filter_by_id(request:Request):    
    try:
        # 从 GET 请求中获取 'device_id' 参数
        device_id = request.query.get('device_id')  # 从查询参数中获取字段        

        if not device_id:
            return HTTPBadRequest(text=json.dumps({"error"}))
        else:
            device = await MySqlConn.rawSqlCmd(f'''SELECT * from devices WHERE id = "{device_id}" ORDER BY id ASC''')
            device_list = [{"device_id": ONE_device[0], "device_name": ONE_device[1], 
                            "device_num": ONE_device[2], "area_id": ONE_device[3], "icon_addr": ONE_device[4]} for ONE_device in device]                
            return HTTPOk(text=json.dumps(device_list))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)})) 

    except Exception as e:
        print(f"Failed to get device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
