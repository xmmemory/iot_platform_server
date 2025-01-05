from aiohttp.web import UrlDispatcher

from . import index, rawSql
from . import blender
from . import get_version, get_user, get_project
from . import get_area, get_device, get_var
from . import get_record

def add_get(router:UrlDispatcher):
    index.add_get(router)
    rawSql.add_get(router)
    blender.add_get(router)
    get_version.add_get(router)
    get_user.add_get(router)
    get_project.add_get(router)
    get_area.add_get(router)
    get_device.add_get(router)
    get_var.add_get(router)
    get_record.add_get(router)
