from aiohttp.web import UrlDispatcher

from . import index, rawSql
from . import blender
from . import latest_version

def add_get(router:UrlDispatcher):
    index.add_get(router)
    rawSql.add_get(router)
    blender.add_get(router)
    latest_version.add_get(router)