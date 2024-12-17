from aiohttp.web import UrlDispatcher
from . import area, login
from . import device, project, insert_device

def add_post(router:UrlDispatcher):
    
    login.add_post(router)
    area.add_post(router)
    device.add_post(router)
    project.add_post(router)
    insert_device.add_post(router)