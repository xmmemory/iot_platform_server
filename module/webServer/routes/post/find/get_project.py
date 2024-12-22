from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json

def add_post(router:UrlDispatcher):
    router.add_post(
        path= '/getProject',
        handler= handle
    )

async def handle(request:Request):
    projects = await MySqlConn.rawSqlCmd("SELECT project_id, project_name from projects ORDER BY project_id ASC")    
    project_list = [{"project_id": project[0], "project_name": project[1]} for project in projects]    
    return HTTPOk(text=json.dumps(project_list))