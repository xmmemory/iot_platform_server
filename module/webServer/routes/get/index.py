from aiohttp.web import UrlDispatcher, Request, HTTPOk

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/index',
        handler= index
    )

async def index(request:Request):   
    return HTTPOk(text="Welcome to 绿如蓝测试 service!")