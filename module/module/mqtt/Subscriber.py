import paho.mqtt.client as mqtt

# 配置 MQTT 服务器的参数

broker_address = "49.232.133.59"  # 云财服务器
port = 7203                      # 113服务器端口
# broker_address = "101.201.60.179"  # 绿如蓝IOT服务器
# port = 8001                      # 绿如蓝服务器端口

topic = "#"            # 要订阅的主题
username = "lrl001"       # 替换为你的用户名
password = "123456"       # 替换为你的密码

# 定义回调函数，当收到消息时触发
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# 创建 MQTT 客户端实例
client = mqtt.Client()

# 设置用户名和密码
client.username_pw_set(username, password)

# 连接到服务器
client.connect(broker_address, port)

# 设置回调函数
client.on_message = on_message
# 订阅主题
client.subscribe(topic)

print(f"Subscribed to topic '{topic}'")

# 开始循环等待消息
client.loop_forever()
