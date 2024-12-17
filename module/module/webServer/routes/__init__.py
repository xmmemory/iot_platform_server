from aiohttp.web import UrlDispatcher

from . import get, post

def add_routes(router:UrlDispatcher):
    get.add_get(router)
    post.add_post(router)