from module.db.mysqlConn import MySqlConn
import aiomqtt
import json
import asyncio
import time
class MqttSubscriber:
    def connect(self, broker_addr:str, broker_port:int, username:str, password:str):
        self.broker_addr = broker_addr
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.topic_list = list()
        self.update_batch = []
        self.counter_acount = 0
        self.counter_last_acount = 0 
        self.counter_cnt = 0
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
        # 使用 perf_counter 获取更高精度的时间差
        # start_time = time.perf_counter()

        payload_dict = json.loads(payload)
        
        self.counter_acount = 0
        for key, value in payload_dict.items():
            if isinstance(value, dict): 
                self.counter_acount += len(value.keys())
            else: 
                self.counter_acount += 1

        if self.counter_last_acount != self.counter_acount:
            print("self.counter_acount update", self.counter_acount)
            self.counter_last_acount = self.counter_acount
            self.counter_cnt = 0


        for key, value in payload_dict.items():
            if isinstance(value, (int, float)):  # 处理简单的键值对
                var_full_code = key
                latest_value = round(value, 1)
                self.update_batch.append((var_full_code, latest_value))
                self.counter_cnt = (self.counter_cnt + 1) % (self.counter_acount + 1)
                if self.counter_cnt == 0:
                    await self.insert_or_create_table(var_full_code, latest_value)

            elif isinstance(value, dict):  # 处理嵌套的布尔值字典
                for sub_key, sub_value in value.items():
                    composite_key = f"{key}.{sub_key}"
                    latest_value = sub_value
                    self.update_batch.append((composite_key, latest_value))
                    self.counter_cnt = (self.counter_cnt + 1) % (self.counter_acount + 1)
                    if self.counter_cnt == 0:
                        await self.insert_or_create_table(composite_key, latest_value)

        # 当积累到一定数量的记录后批量执行更新
        if len(self.update_batch) >= 20:  # 比如积累20条数据后执行一次更新
            # print(self.update_batch)
            await self.batch_update(self.update_batch)
            self.update_batch.clear()  # 清空批量数据

        # # 计算时间差
        # end_time = time.perf_counter()
        # execution_time = end_time - start_time
        # print(f"Execution time: {execution_time:.4f} seconds")

        

    async def batch_update(self, updates):
        # 组装 SQL 语句
        sql = "UPDATE vars SET latest_value = CASE var_full_code "
        for var_full_code, latest_value in updates:
            sql += f"WHEN '{var_full_code}' THEN '{latest_value}' "
        sql += "END WHERE var_full_code IN (" + ",".join([f"'{var_full_code}'" for var_full_code, _ in updates]) + ")"
        
        # 执行批量更新
        await MySqlConn.rawSqlCmd(sql)

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
