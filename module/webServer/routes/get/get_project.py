from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_get(router:UrlDispatcher):
    router.add_get(
        path = '/projects',
        handler = get_all_projects
    )
    router.add_get(
        path = '/project/f',
        handler = get_project_by_id
    )

async def get_all_projects(request:Request):
    projects = await MySqlConn.rawSqlCmd("SELECT id, name from projects ORDER BY id ASC")    
    project_list = [{"project_id": project[0], "project_name": project[1]} for project in projects]    
    return HTTPOk(text=json.dumps(project_list))

async def get_project_by_id(request: Request):
    user_name = request.query.get('user_name')
    if not user_name:
        return HTTPBadRequest(text="user_name parameter is required")

    try:
        # Step 1: Get user_id from users table
        user_result = await MySqlConn.rawSqlCmd(f'SELECT id FROM users WHERE name = "{user_name}"')
        if not user_result:
            return HTTPBadRequest(text="User not found")

        user_id = user_result[0][0]

        # Step 2: Get project_ids from project_users table
        project_users_result = await MySqlConn.rawSqlCmd(f'SELECT project_id FROM project_users WHERE user_id = "{user_id}"')
        if not project_users_result:
            return HTTPBadRequest(text=json.dumps([]))

        project_ids = [project[0] for project in project_users_result]
        print("project_ids", project_ids)

        # Step 3: Get project details from projects table
        project_ids_str = ','.join(map(str, project_ids))  # 将 project_ids 转换为字符串，并以逗号分隔
        query = f"SELECT id, name FROM projects WHERE id IN ({project_ids_str}) ORDER BY id ASC"
        projects_result = await MySqlConn.rawSqlCmd(query)
        if projects_result is None:
            print("查询失败，请检查日志。")
        else:
            print("查询成功：", projects_result)

        project_list = [{"project_id": project[0], "project_name": project[1]} for project in projects_result]

        print("project_list", project_list)

        return HTTPOk(text=json.dumps(project_list))

    except Exception as e:
        return HTTPBadRequest(text=str(e))
    
