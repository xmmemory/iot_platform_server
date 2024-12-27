from aiohttp.web import UrlDispatcher

from . import index, rawSql
from . import blender
from . import latest_version
from . import get_project, get_area, get_device

def add_get(router:UrlDispatcher):
    index.add_get(router)
    rawSql.add_get(router)
    blender.add_get(router)
    latest_version.add_get(router)
    get_project.add_get(router)
    get_area.add_get(router)
    get_device.add_get(router)