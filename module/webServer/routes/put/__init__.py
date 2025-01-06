from aiohttp.web import UrlDispatcher

from . import put_area, put_device, put_var

def add_put(router:UrlDispatcher):
    put_area.add_put(router)
    put_device.add_put(router)
    put_var.add_put(router)