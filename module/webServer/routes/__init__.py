from aiohttp.web import UrlDispatcher

from . import get, post, put

def add_routes(router:UrlDispatcher):
    get.add_get(router)
    post.add_post(router)
    put.add_post(router)