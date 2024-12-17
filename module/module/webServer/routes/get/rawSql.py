from aiohttp.web import UrlDispatcher

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/rawSql',
        handler= handle
    )

from aiohttp.web import Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
from json import dumps

async def handle(request:Request):
    sqlQuery = request.query['sql'][1:-1] # str => int(a) => list(a)
    # print(sqlQuery)
    # sqlQuery = "select * from * where "
    result = await MySqlConn.rawSqlCmd(sqlQuery)

    if not isinstance(result, str): result = dumps(result)
    return HTTPOk(text=result)