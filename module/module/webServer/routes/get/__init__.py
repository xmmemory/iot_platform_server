from aiohttp.web import UrlDispatcher

from . import index, rawSql
from . import blender

def add_get(router:UrlDispatcher):
    index.add_get(router)
    rawSql.add_get(router)
    blender.add_get(router)