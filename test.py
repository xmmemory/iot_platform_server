from module.mqtt.subscriber import MqttSubscriber
import asyncio

async def main():
    loop = asyncio.get_event_loop()
    mqtt = MqttSubscriber().connect("101.201.60.179", 1883, "lrl001", "123456")
    mqtt.subscribe("#")
    await mqtt.listen()



asyncio.run(main())
# import requests 
# resp = requests.post("http://127.0.0.1:9013/login", json={"username": "lrl001","password": "123"})
# print(resp, resp.text)