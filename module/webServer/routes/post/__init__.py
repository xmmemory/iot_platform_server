from aiohttp.web import UrlDispatcher

from .find import get_area, get_device, get_project, get_var
from .modify import modify_area, modify_device, modify_var
from .control import control_var
from .find import get_version, get_VarValue
from . import login
from . import post_user

def add_post(router:UrlDispatcher):
    
    login.add_post(router)
    get_area.add_post(router)
    get_device.add_post(router)
    get_project.add_post(router)
    get_var.add_post(router)
    modify_device.add_post(router)
    modify_area.add_post(router)
    modify_var.add_post(router)
    control_var.add_post(router)
    get_version.add_post(router)
    get_VarValue.add_post(router)
    post_user.add_post(router)
    