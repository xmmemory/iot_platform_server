from aiohttp.web import UrlDispatcher, Request, HTTPOk, HTTPBadRequest
from module.db.mysqlConn import MySqlConn
from module.mqtt.publisher import MqttPublisher
from typing import Dict
import json

def add_put(router: UrlDispatcher):
    router.add_put(
        path='/update/var',
        handler=update_var
    )
    router.add_put(
        path='/modify/var',
        handler=modify_var
    )

async def update_var(request: Request):
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
            
        elif command == "update_value":
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

async def modify_var(request: Request):
    try:
        data: dict = await request.json()

        var_name = data.get("var_name")
        simple_code = data.get("var_code")
        var_type = data.get("var_type")
        var_permission = data.get("var_permission")
        device_id = data.get("device_id")
        var_id = data.get("var_id")
        var_full_code = data.get("var_full_code")

        if (var_name and var_name.strip() and simple_code is not None and var_type and var_type.strip() and var_permission and var_permission.strip() and device_id is not None):
            print(var_name, simple_code, var_type, var_permission, device_id, var_id)
        else:
            print("modify var insufficient data:", var_name, simple_code, var_type, var_permission, device_id, var_id)
            return HTTPBadRequest(text="upload data is not enough.") 

        res = await MySqlConn.rawSqlCmd(
                f'''UPDATE device_variables SET
                var_name = "{var_name}",
                simple_code = "{simple_code}",
                var_type = "{var_type}",
                var_permission = "{var_permission}",
                device_id = "{device_id}",
                var_full_code = "{var_full_code}"
                WHERE id = {var_id}''')
        print(res)
        return HTTPOk(text=json.dumps(res))
                    
    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return HTTPBadRequest(text=json.dumps({"error": str(ve)}))

    except Exception as e:
        print(f"Failed to insert vars data: {str(e)}")
        return HTTPBadRequest(text=json.dumps({"error": str(e)})) 