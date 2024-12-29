from aiohttp.web import UrlDispatcher

from . import put_var

def add_put(router:UrlDispatcher):
    put_var.add_put(router)