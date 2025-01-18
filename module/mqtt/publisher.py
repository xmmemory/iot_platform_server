import aiomqtt
import json

class MqttPublisher:
    def __init__(self, broker_addr: str, broker_port: int, username: str, password: str):
        self.broker_addr = broker_addr
        self.broker_port = broker_port
        self.username = username
        self.password = password

    async def publish(self, topic: str, payload: dict):
        async with aiomqtt.Client(hostname=self.broker_addr, port=self.broker_port,
                                  username=self.username, password=self.password) as client:
            # 将字典 payload 转换为 JSON 字符串
            payload_str = json.dumps(payload)
            await client.publish(topic, payload_str)
            print(f"Message published to topic '{topic}': {payload_str}")        
