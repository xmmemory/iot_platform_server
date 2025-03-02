from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/areas',
        handler= get_all_areas
    )
    router.add_get(
        path= '/api/areas',
        handler= api_get_areas
    )

async def get_all_areas(request:Request):
    areas = await MySqlConn.rawSqlCmd("SELECT id, area_name from areas ORDER BY id ASC")
    area_list = [{"area_id": area[0], "area_name": area[1]} for area in areas]
    return HTTPOk(text=json.dumps(area_list))


async def api_get_areas(request: Request):
    try:
        # 解析分页参数
        page = int(request.query.get('page', 1))
        page_size = int(request.query.get('pageSize', 10))
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 执行分页查询
        areas = await MySqlConn.rawSqlCmd(
            f"SELECT id, area_name FROM areas ORDER BY id ASC LIMIT {page_size} OFFSET {offset}"
        )
        
        # 查询总记录数
        total_count_query = await MySqlConn.rawSqlCmd("SELECT COUNT(*) FROM areas")
        total_count = total_count_query[0][0] if total_count_query else 0
        
        # 构建响应数据
        area_list = [
            {
                "area_id": area[0], 
                "area_name": area[1]
            } for area in areas
        ]
        
        response_data = {
            "data": area_list,
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
        print(f"Failed to get area data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))