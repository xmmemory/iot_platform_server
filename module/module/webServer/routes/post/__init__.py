from aiohttp.web import UrlDispatcher

from .find import area, device, project, var
from .insert import modify_area, modify_device, modify_var
from . import login

def add_post(router:UrlDispatcher):
    
    login.add_post(router)
    area.add_post(router)
    device.add_post(router)
    project.add_post(router)
    var.add_post(router)
    modify_device.add_post(router)
    modify_area.add_post(router)
    modify_var.add_post(router)