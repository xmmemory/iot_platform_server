from aiohttp.web import UrlDispatcher

from . import add_area, add_device, add_var
from ..PUT import put_var
from . import login
from . import add_user

def add_post(router:UrlDispatcher):
    
    login.add_post(router)
    add_user.add_post(router)
    add_area.add_post(router)
    add_device.add_post(router)
    add_var.add_post(router)
    put_var.add_post(router)
    