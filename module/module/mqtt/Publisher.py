import paho.mqtt.client as mqtt 


class MqttPublisher:
    def __init__(self):
        self.client = mqtt.Client()

    def connect(self, broker_addr:str, broker_port:int, username:str, password:str):
        self.client.username_pw_set(username, password)
        self.client.connect(broker_addr, broker_port)

    def disconnect(self):
        self.client.disconnect()
    
    def public(self, topic:str, payload:str):
        self.client.publish(topic, payload)


"""
# 配置 MQTT 服务器的参数
broker_address = "49.232.133.59"  # 云财服务器
port = 7203                      # 113服务器端口
# broker_address = "101.201.60.179"  # 绿如蓝IOT服务器
# port = 1883                      # 绿如蓝服务器端口


topic = "/DownloadTopic"            # 要发布的主题
username = "lrl001"       # 替换为你的用户名
password = "123456"       # 替换为你的密码

# 创建 MQTT 客户端实例
client = mqtt.Client()

# 设置用户名和密码
client.username_pw_set(username, password)

# 连接到服务器
client.connect(broker_address, port)

# 发布消息
# message = '''{
#   "rw_prot": {
#     "Ver": "1.0.1",
#     "dir": "down",
#     "id": "101",
#     "r_data": [{"name": "DI1"},{"name": "DO1"}],
#     "w_data": [{"name": "DO1", "value": "0"}]
#   }
# }'''
message = '''{"rw_prot": {"Ver": "1.0.1","dir": "down","id": "101","r_data": [{"name": "DI1"},{"name": "DO1"},{"name": "DO2"}],"w_data": [{"name": "DO1", "value": "0"}]}}'''
try:
    data = json.loads(message)
    print(data)
except json.JSONDecodeError as e:
    print(f"JSON解析错误:{e}")
# message = "df11"
client.publish(topic, message)

print(f"published to topic '{topic}'")

# 断开与服务器的连接
client.disconnect()
"""