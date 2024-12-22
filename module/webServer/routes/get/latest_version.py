from aiohttp.web import UrlDispatcher, Request, HTTPOk

def add_get(router:UrlDispatcher):
    router.add_get(
        path= '/api/latest-version',
        handler= index
    )

async def index(request:Request):   
    return HTTPOk(text="2.0.1")