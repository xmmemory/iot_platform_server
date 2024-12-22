# db.py
import aiomysql
import asyncio

class MySQLAsyncConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.pool = None

    async def connect(self):
        """使用连接池来管理连接"""
        self.pool = await aiomysql.create_pool(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True
        )
        print("成功连接到数据库")

    async def close(self):
        """关闭连接池"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            print("数据库连接池已关闭")

    async def execute_query(self, query, params=None):
        """使用连接池获取连接并执行查询"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                await conn.commit()

    async def fetch_all(self, query, params=None):
        """使用连接池获取连接并返回查询结果"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchall()

# 创建并初始化连接池的实例
y_async_db = MySQLAsyncConnection(
    host="localhost", 
    user="root", 
    password="FORever1437", 
    database="lvrulan_mysql"
)

async def init_db():
    """在主程序开始时初始化数据库连接"""
    await y_async_db.connect()

async def close_db():
    """在主程序结束时关闭数据库连接池"""
    await y_async_db.close()
