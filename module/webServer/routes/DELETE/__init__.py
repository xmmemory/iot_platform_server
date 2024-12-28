from aiohttp.web import UrlDispatcher

from . import delete_user

def add_delete(router:UrlDispatcher):    
    delete_user.add_delete(router)