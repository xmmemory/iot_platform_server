from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
from datetime import datetime
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/record/var/f',
        handler= get_recode_by_var_name
    )
    
async def get_recode_by_var_name(request:Request):
    try:
        # 从 GET 请求中获取 'device_id' 参数
        full_code = request.query.get('full_code')  # 从查询参数中获取字段
        start_date_str = request.query.get('start_date')  # 获取开始时间
        end_date_str = request.query.get('end_date')  # 获取结束时间
        data_length = request.query.get('data_length')

        # 用下划线替换点号，避免表名错误
        table_name = f"var_{full_code.replace('.', '_')}"

        # 构造 SQL 查询
        query = f'''SELECT value, created_at FROM {table_name} WHERE 1=1'''

        # 如果提供了开始时间，则添加时间范围过滤
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str)  # 转换为 datetime 对象
                query += f" AND created_at >= '{start_date.isoformat()}'"
            except ValueError:
                raise ValueError(f"Invalid start_date format: {start_date_str}")
            
        # 如果提供了结束时间，则添加时间范围过滤
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str)  # 转换为 datetime 对象
                query += f" AND created_at <= '{end_date.isoformat()}'"
            except ValueError:
                raise ValueError(f"Invalid end_date format: {end_date_str}")

        if data_length:    
            query += f" ORDER BY id DESC LIMIT {data_length}"
        else:
            query += f" ORDER BY id DESC LIMIT 20"
        
        # 执行查询
        vars = await MySqlConn.rawSqlCmd(query)
        
        # print(vars)
        var_list = [{"value": var[0], "created_at": var[1]} for var in vars]
        # print(var_list)
        # 转换 datetime 为字符串
        for item in var_list:
            if item['created_at'] is not None:
                item['created_at'] = item['created_at'].isoformat()
            else:
                item['created_at'] = ""  # 或者设置为一个默认的日期字符串
        return HTTPOk(text=json.dumps(var_list))
    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to modify var data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
