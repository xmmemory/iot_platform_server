from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
import json
from module.mqtt.publisher import MqttPublisher
import asyncio
from typing import Dict

def add_post(router: UrlDispatcher):
    router.add_post(
        path='/controlVar',
        handler=control
    )
async def control(request: Request):
    try:
        data: dict = await request.json()
    
        command = data.get('command')
        var_full_code = data.get("var_full_code")
        new_var_value = data.get("new_var_value")

        mqtt = MqttPublisher("101.201.60.179", 1883, "lrl001", "123456")   

        if command == "flip_switch":
            # 根据 var_full_code 分割，假设是 'M3.5' 需要分割成 'M3' 和 '5'
            prefix, suffix = var_full_code.split('.')

            # 将 new_var_value 转换为布尔值，'True' -> True, 'False' -> False
            bool_value = True if new_var_value == 'True' else False

            # 构建嵌套字典 payload
            payload: Dict[str, dict] = {}

            if prefix not in payload:
                payload[prefix] = {}

            payload[prefix][suffix] = bool_value

            # 发布消息
            await mqtt.publish("40800965", payload)

            return HTTPOk(text="控制指令下发")
            
        elif command == "modify_value":
            try:
                if '.' in new_var_value:
                    new_var_value = float(new_var_value)  # 转换为浮动类型
                else:
                    new_var_value = int(new_var_value)  # 转换为整数类型
            except ValueError:
                # 如果转换失败，则保持原值为字符串
                pass

            # 构建简单字典 payload
            payload: Dict[str, any] = {
                var_full_code: new_var_value
            }

            # 发布消息
            await mqtt.publish("40800965", payload)

            return HTTPOk(text="变量编辑指令下发") 
                
        else:
            return HTTPBadRequest(text="unknow error.")
        
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to insert vars data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)}))
    