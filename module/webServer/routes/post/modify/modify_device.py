from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/modifyDevice',
        handler=modify
    )

async def modify(request: Request):
    try:
        data: dict = await request.json()

        command = data.get('command')

        device_id = data.get("device_id")
        device_name = data.get("device_name")
        device_num = data.get("device_num")
        area_id = data.get("area_id")

        if command == "del_device" and device_id is not None:
            result = await MySqlConn.rawSqlCmd(f'''SELECT * FROM devices WHERE id = "{device_id}"''')
            if not result:
                return HTTPBadRequest(text="No record found for deletion.")
            else:
                res = await MySqlConn.rawSqlCmd(f'''DELETE FROM devices WHERE id ="{device_id}" LIMIT 1''')
                return HTTPOk(text=json.dumps(res))

        if device_name and device_name.strip() and device_num is not None and area_id is not None:
            print(command, device_name, device_num, area_id, device_id)
        else:
            print(command, "insufficient data:", device_name, device_num, area_id, device_id)
            return HTTPBadRequest(text="upload data is not enough.") 

        if command == "insert_device":
            # TODO 应该在插入数据之前，首先判断是否存在相同设备
            if 1:             
                data = await MySqlConn.rawSqlCmd(
                f'INSERT INTO devices (device_name, device_num, area_id) VALUES ("{device_name}",{device_num}, {area_id})')
                print(data)
                return HTTPOk(text=json.dumps(data))
            else:
                return HTTPBadRequest(text="insert device fail, device is exist.")        
                    
        elif command == "update_device":
            data = await MySqlConn.rawSqlCmd(
                    f'''UPDATE devices SET device_name = "{device_name}", device_num = "{device_num}", area_id = "{area_id}" WHERE id = {device_id}''')
            print(data)
            return HTTPOk(text=json.dumps(data))
            
        
        else:
            return HTTPBadRequest(text="unknow error.")
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))