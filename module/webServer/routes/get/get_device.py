from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/devices',
        handler= get_all_devices
    )
    router.add_get(
        path= '/device/f',
        handler= get_device_by_id
    )
    # api
    router.add_get(
        path= '/api/devices',
        handler= api_get_devices
    )
    router.add_get(
        path= '/api/devices/status',
        handler= api_get_devices_status
    )

async def api_get_devices(request: Request):
    try:
        # 解析分页参数
        page = int(request.query.get('page', 1))
        page_size = int(request.query.get('pageSize', 10))
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 执行分页查询
        devices = await MySqlConn.rawSqlCmd(
            f"SELECT id, device_name, device_sn, area_id, icon_addr, status FROM devices ORDER BY id ASC LIMIT {page_size} OFFSET {offset}"
        )

        # 查询总记录数
        total_count_query = await MySqlConn.rawSqlCmd("SELECT COUNT(*) FROM devices")
        total_count = total_count_query[0][0] if total_count_query else 0
        
        
        # 构建响应数据
        device_list = [
            {
                "device_id": device[0], 
                "device_name": device[1], 
                "device_sn": device[2], 
                "area_id": device[3], 
                "icon_addr": device[4], 
                "status": device[5]
            } for device in devices
        ]
        
        response_data = {
            "data": device_list,
            "pagination": {
                "page": page,
                "pageSize": page_size,
                "total": total_count
            }
        }
        
        return HTTPOk(text=json.dumps(response_data))
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))
    
    except Exception as e:
        print(f"Failed to get device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))

async def api_get_devices_status(request:Request):
    devices = await MySqlConn.rawSqlCmd("SELECT id, status from devices ORDER BY id ASC")
    device_list = [{"device_id": device[0], "status": device[1]} for device in devices]
    # 查询总记录数
    total_count_query = await MySqlConn.rawSqlCmd("SELECT COUNT(*) FROM devices")
    total_count = total_count_query[0][0] if total_count_query else 0        
    response_data = {
            "data": device_list,
            "pagination": {
                "total": total_count
            }
        }
    return HTTPOk(text=json.dumps(response_data))

async def get_all_devices(request:Request):
    devices = await MySqlConn.rawSqlCmd("SELECT id, device_name, device_sn, area_id, icon_addr, status from devices ORDER BY id ASC")
    device_list = [{"device_id": device[0], "device_name": device[1], 
                    "device_sn": device[2], "area_id": device[3], "icon_addr": device[4], "status": device[5]} for device in devices]
    return HTTPOk(text=json.dumps(device_list))

async def get_device_by_id(request:Request):    
    try:
        # 从 GET 请求中获取 'device_id' 参数
        device_id = request.query.get('device_id')  # 从查询参数中获取字段        

        if not device_id:
            return HTTPBadRequest(text=json.dumps({"error"}))
        else:
            device = await MySqlConn.rawSqlCmd(f'''SELECT id, device_name, device_sn, area_id, icon_addr, status from devices WHERE id = "{device_id}" ORDER BY id ASC''')
            device_list = [{"device_id": ONE_device[0], "device_name": ONE_device[1], 
                            "device_sn": ONE_device[2], "area_id": ONE_device[3], "icon_addr": ONE_device[4], "status": ONE_device[5]} for ONE_device in device]                
            return HTTPOk(text=json.dumps(device_list))
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)})) 

    except Exception as e:
        print(f"Failed to get device data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
