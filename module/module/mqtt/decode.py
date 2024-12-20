from module.db.mysqlConn import MySqlConn
import asyncio

def msg_callback(client, userdata, message):
    # print(f"Received message `{message.payload.decode()}` on topic `{message.topic}`")
    asyncio.create_task(MySqlConn.rawSqlCmd(f'INSERT INTO test (value) VALUES ("{message.payload.decode()}")'))