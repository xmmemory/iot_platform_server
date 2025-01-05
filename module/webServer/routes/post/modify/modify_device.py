from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/modifyDevice',
        handler=modify
    )

    router.add_post(
        path='/create/device',
        handler=create_device
    )

async def modify(request: Request):
    try:
        data: dict = await request.json()

        command = data.get('command')

        device_id = data.get("device_id")
        device_name = data.get("device_name")
        device_num = data.get("device_num")
        area_id = data.get("area_id")
        icon_addr = data.get("icon_addr")

        if command == "del_device" and device_id is not None:
            result = await MySqlConn.rawSqlCmd(f'''SELECT * FROM devices WHERE id = "{device_id}"''')
            if not result:
                return HTTPBadRequest(text="No record found for deletion.")
            else:
                res = await MySqlConn.rawSqlCmd(f'''DELETE FROM devices WHERE id ="{device_id}" LIMIT 1''')
                return HTTPOk(text=json.dumps(res))

        if device_name and device_name.strip() and area_id is not None:
            print(command, device_name, device_num, area_id, device_id, icon_addr)
        else:
            print(command, "insufficient data:", device_name, device_num, area_id, device_id, icon_addr)
            return HTTPBadRequest(text="upload data is not enough.") 

        if command == "insert_device":
            # TODO 应该在插入数据之前，首先判断是否存在相同设备
            if 1:
                res = await MySqlConn.rawSqlCmd(
                f'INSERT INTO devices (device_name, device_num, area_id, icon_addr) VALUES ("{device_name}",{device_num}, {area_id}, "{icon_addr}")')
                print(res)
                return HTTPOk(text=json.dumps(res))
            else:
                return HTTPBadRequest(text="insert device fail, device is exist.")        
                    
        elif command == "update_device":
            res = await MySqlConn.rawSqlCmd(
                    f'''UPDATE devices SET device_name = "{device_name}", device_num = "{device_num}", area_id = "{area_id}", icon_addr= "{icon_addr}" WHERE id = {device_id}''')
            print(res)            
            return HTTPOk(text=json.dumps(res))
        
        else:
            return HTTPBadRequest(text="unknow error.")
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))


async def create_device(request: Request):
    try:
        data: dict = await request.json()

        command = data.get('command')

        device_id = data.get("device_id")
        device_name = data.get("device_name")
        device_num = data.get("device_num")
        area_id = data.get("area_id")
        icon_addr = data.get("icon_addr")

        if command == "del_device" and device_id is not None:
            result = await MySqlConn.rawSqlCmd(f'''SELECT * FROM devices WHERE id = "{device_id}"''')
            if not result:
                return HTTPBadRequest(text="No record found for deletion.")
            else:
                res = await MySqlConn.rawSqlCmd(f'''DELETE FROM devices WHERE id ="{device_id}" LIMIT 1''')
                return HTTPOk(text=json.dumps(res))

        if device_name and device_name.strip() and area_id is not None:
            print(command, device_name, device_num, area_id, device_id, icon_addr)
        else:
            print(command, "insufficient data:", device_name, device_num, area_id, device_id, icon_addr)
            return HTTPBadRequest(text="upload data is not enough.") 

        if command == "insert_device":
            # TODO 应该在插入数据之前，首先判断是否存在相同设备
            if 1:
                res = await MySqlConn.rawSqlCmd(
                f'INSERT INTO devices (device_name, device_num, area_id, icon_addr) VALUES ("{device_name}",{device_num}, {area_id}, "{icon_addr}")')
                print(res)
                return HTTPOk(text=json.dumps(res))
            else:
                return HTTPBadRequest(text="insert device fail, device is exist.")        
                    
        elif command == "update_device":
            res = await MySqlConn.rawSqlCmd(
                    f'''UPDATE devices SET device_name = "{device_name}", device_num = "{device_num}", area_id = "{area_id}", icon_addr= "{icon_addr}" WHERE id = {device_id}''')
            print(res)            
            return HTTPOk(text=json.dumps(res))
        
        else:
            return HTTPBadRequest(text="unknow error.")
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))