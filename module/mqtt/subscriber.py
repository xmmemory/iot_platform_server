from module.db.mysqlConn import MySqlConn
import aiomqtt
import json
import asyncio

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
        try:
            async with aiomqtt.Client(hostname=self.broker_addr, port=self.broker_port,
                                        username=self.username, password=self.password) as client:
                for topic in self.topic_list: await client.subscribe(topic)
                async for message in client.messages:
                    topic, payload = message.topic, message.payload.decode()
                    await self.message_callback(topic, payload)
        except asyncio.CancelledError:
            print("listen Cancelled.")
            raise

    async def message_callback(self, topic: str, payload: str):
        payload_dict = json.loads(payload)
        for key, value in payload_dict.items():
            if isinstance(value, (int, float)):  # 处理简单的键值对
                var_full_code = key
                latest_value = round(value, 1)
                # 
                sql = f'''
                    UPDATE vars 
                    SET latest_value = "{latest_value}"
                    WHERE var_full_code = "{var_full_code}"
                '''
                await MySqlConn.rawSqlCmd(sql)
                # 使用 insert_or_create_table 函数来创建表并插入数据
                await self.insert_or_create_table(var_full_code, latest_value)

            elif isinstance(value, dict):  # 处理嵌套的布尔值字典
                for sub_key, sub_value in value.items():
                    composite_key = f"{key}.{sub_key}"
                    latest_value = sub_value
                    # 
                    sql = f'''
                        UPDATE vars 
                        SET latest_value = "{latest_value}"
                        WHERE var_full_code = "{composite_key}"
                    '''
                    await MySqlConn.rawSqlCmd(sql)
                    # 使用 insert_or_create_table 函数来创建表并插入数据
                    await self.insert_or_create_table(composite_key, latest_value)

    async def insert_or_create_table(self, var_full_code: str, value: str):
        # 用下划线替换点号，避免表名错误
        table_name = f"var_{var_full_code.replace('.', '_')}"

        # 检查表是否已存在
        check_table_sql = f"SHOW TABLES LIKE '{table_name}'"
        result = await MySqlConn.rawSqlCmd(check_table_sql)

        # 如果表不存在，则创建表
        if not result:
            # SQL: 创建表，如果不存在
            sql_create = f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    value VARCHAR(255) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''
            await MySqlConn.rawSqlCmd(sql_create)
        
        # 在插入数据前，查询表中最后一行的值
        sql_select_last_value = f'''
            SELECT value FROM {table_name} ORDER BY id DESC LIMIT 1
        '''
        last_value_result = await MySqlConn.rawSqlCmd(sql_select_last_value)
        
        # 判断表中最后的值是否与当前值一致
        if last_value_result:
            if str(last_value_result[0][0]) == str(value):  # 转换为 string 进行比较
                return  # 如果值相同，跳过插入操作
                
        # SQL: 插入数据，数据库会自动记录当前时间戳
        sql_insert = f'''
            INSERT INTO {table_name} (value)
            VALUES ("{value}")
        '''
        await MySqlConn.rawSqlCmd(sql_insert)
