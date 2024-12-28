from aiohttp.web import UrlDispatcher

from . import GET, DELETE, POST, PUT

def add_routes(router:UrlDispatcher):
    DELETE.add_delete(router)
    GET.add_get(router)
    POST.add_post(router)
    # PUT.add_put(router)