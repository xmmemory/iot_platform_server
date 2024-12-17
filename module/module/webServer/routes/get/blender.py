import asyncio
import json
from module.db.mysqlConn import MySqlConn

from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest

#连接到MQTT代理

def add_get(router: UrlDispatcher):

    # TODO
    # 可能需要再规划路由
    router.add_get('/blender/set_duration', set_duration) # /set_duration?duration=(int)str "123"
    router.add_get('/blender/start', start_blender)
    router.add_get('/blender/status', status_blender)


async def set_duration(request: Request):
    # duration = request.query.get('duration', type=int)
    duration = request.query.get('duration')

    # 是不是需要通过什么方式指示设备
    device_num = request.query.get('device_num')

    if not isinstance(duration, str) or not duration.isdigit() or not (0 <= int(duration) <= 60):
        return HTTPBadRequest(text="Duration must be between 0 and 60 minutes.")
    duration = int(duration)
    #从数据库查询设备功能码
    # db = MySqlConn(host='',user='lvrulan1',password='Lvrulan123',databases='')
    # db.openConn()    

    sql = "SELECT function_code FROM devices WHERE device_num = %s"
    result = MySqlConn.rawSqlCmd(sql,(device_num)) # result = [] or None
    if not result :
        # db.closeConn()
        return HTTPBadRequest(text=f"No device found with device number:{device_num}")
    function_code = result[0][0]
    # db.closeConn
    #组装mqtt消息(具体还要再问熊哥)
    msg ={
        "topic":{
            function_code:{
                "action":"start"
            }
        }
    }
    #发布MQTT消息
    # TODO
    # mqtt 发送设置运行时间指令到设备
    # 流程：
    # 首先要根据用户的需求去表里面查设备的"功能码" 如：command = mysqlConn.rawSqlCmd(sql语句)
    # 根据mqtt报文协议格式，组成信息，如：msg = {"topic":{"M3":{"5":True}}
    # 类似这样的函数 mqtt.publisher.publish(msg) 去把信息发布出去
    

    # TODO
    # text 可能需要更换成 app/小程序 可以解析的回复（具体再商议）
    text = f"Blender No.{device_num}, Duration set to {duration} minutes."
    return HTTPOk(text=text)

async def start_blender(request: Request):

    # TODO
    # mqtt 发送开始指令到设备

    # TODO
    # 更换成 app/小程序 可以解析的回复
    return HTTPOk(text=f"Blender started.")

async def status_blender(request: Request):
    status = None
    
    # TODO
    # 从mysql数据库查询设备运行状态
    # 获取运行状态 status

    # TODO
    # 更换成 app/小程序 可以解析的回复
    return HTTPOk(text=f"Blender's status is {status}.")