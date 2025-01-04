from aiohttp.web import UrlDispatcher

from .modify import modify_area, modify_device, modify_var
from .control import control_var
from . import login
from . import post_user

def add_post(router:UrlDispatcher):
    
    login.add_post(router)
    modify_device.add_post(router)
    modify_area.add_post(router)
    modify_var.add_post(router)
    control_var.add_post(router)
    post_user.add_post(router)
    