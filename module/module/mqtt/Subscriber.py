from module.db.mysqlConn import MySqlConn
import aiomqtt

class MqttSubscriber:
    def connect(self, broker_addr:str, broker_port:int, username:str, password:str):
        self.broker_addr = broker_addr
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.topic_list = list()
        return self

    def subscribe(self, topic:str):
        self.topic_list.append(topic)
    
    async def listen(self):
        async with aiomqtt.Client(hostname=self.broker_addr, port=self.broker_port,
                                     username=self.username, password=self.password) as client:
            for topic in self.topic_list: await client.subscribe(topic)
            async for message in client.messages:
                topic, payload = message.topic, message.payload.decode()
                await self.message_callback(topic, payload)

    async def message_callback(self, topic: str, payload: str):
        payload_list = payload
        res = await MySqlConn.rawSqlCmd(f'INSERT INTO test (value) VALUES ("{{payload_list}}")')
        print(res)


# # 配置 MQTT 服务器的参数

# # broker_address = "49.232.133.59"  # 云财服务器
# # port = 7203                      # 113服务器端口
# broker_address = "101.201.60.179"  # 绿如蓝IOT服务器
# port = 1883                      # 绿如蓝服务器端口

# topic = "#"            # 要订阅的主题
# username = "lrl001"       # 替换为你的用户名
# password = "123456"       # 替换为你的密码

# # 定义回调函数，当收到消息时触发
# def on_message(client, userdata, message):
#     print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# # 创建 MQTT 客户端实例
# client = mqtt.Client()

# # 设置用户名和密码
# client.username_pw_set(username, password)

# # 连接到服务器
# client.connect(broker_address, port)

# # 设置回调函数
# client.on_message = on_message
# # 订阅主题
# client.subscribe(topic)

# print(f"Subscribed to topic '{topic}'")

# # 开始循环等待消息
# client.loop_forever()