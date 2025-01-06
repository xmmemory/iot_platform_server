from aiohttp.web import UrlDispatcher

from . import delete_user, delete_area, delete_device, delete_var

def add_delete(router:UrlDispatcher):    
    delete_user.add_delete(router)
    delete_area.add_delete(router)
    delete_device.add_delete(router)
    delete_var.add_delete(router)
    