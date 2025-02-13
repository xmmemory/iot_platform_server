import aiomysql
from functools import wraps


class MySqlConn:
    mysqlConnDict:dict[str, aiomysql.pool.Pool] = {}
    nowDbName:str = None
    _pool = None

    @classmethod
    async def openConn(cls, host:str, port:int, user:str, password:str, db_name:str):
        try:
            cls._pool = await aiomysql.create_pool(host = host, port = port, user = user,
                                              password = password, db = db_name)
            MySqlConn.mysqlConnDict[db_name] = cls._pool
            print(f"\033[1;32mMysql database {db_name} connection opened.\033[0m")
            print(f"\033[1;30m", end='')
            print(f"  -- host:    {host}")
            print(f"  -- port:    {port}")
            print(f"  -- user:    {user}")
            print(f"  -- db:      {db_name}")
            print("\033[0m")
        except Exception as e:
            print(f"\033[1;31mError occurred while open Conn:\033[0m {e}")


    @classmethod
    async def closeConn(cls, db_name: str):
        try:
            db = MySqlConn.mysqlConnDict.pop(db_name)
        except KeyError:
            return print(f"\033[1;31mMysql database {db_name} is not connected.\033[0m")
        db.close()
        await db.wait_closed()
        print(f"\033[1;33mMysql database `{db_name}` connection closed.\033[0m")
        
    @classmethod
    def useDb(cls, db_name: str):
        if db_name not in MySqlConn.mysqlConnDict:
            return print(f"\033[1;31mMysql database {db_name} is not connected.\033[0m")
        MySqlConn.nowDbName = db_name
    
    def with_cursor():
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    async with MySqlConn.mysqlConnDict[MySqlConn.nowDbName].acquire() as conn:
                        if not isinstance(conn, aiomysql.connection.Connection):
                            raise TypeError("Expected connection object")
                        async with conn.cursor() as cursor:
                            res = await func(cursor, *args, **kwargs)
                            await conn.commit()
                    return res
                except Exception as e:
                    print(f"Error executing query: {e}")
                    raise
            return wrapper
        return decorator
    
    def transactional_with_cursor():
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                async with MySqlConn.mysqlConnDict[MySqlConn.nowDbName].acquire() as conn:
                    try:
                        if not isinstance(conn, aiomysql.connection.Connection):
                            raise TypeError("Expected connection object")
                        await conn.begin()
                        async with conn.cursor() as cursor:
                            result = await func(cursor, *args, **kwargs)
                        await conn.commit()
                        return result                    
                    except Exception as e:
                        await conn.rollback()
                        print(f"Transaction rolled back due to error: {e}")
                        raise
            return wrapper
        return decorator

    
    @classmethod
    async def execute(cls, query, *args):
        if cls._pool:
            async with cls._pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args)
                    await conn.commit()
                    return cur.rowcount
        return 0


    @with_cursor()
    async def rawSqlCmd(cursor:aiomysql.cursors.Cursor, query:str):
        try:
            n = await cursor.execute(query)
        except Exception as e:
            return print(f"\033[1;31mError occurred when execute query `{query}`. {e}.\033[0m")
        return await cursor.fetchall()
    
    
    @with_cursor()
    async def createTable(cursor:aiomysql.cursors.Cursor, table_name:str):
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            operation_type VARCHAR(50) NOT NULL,
            operation_value VARCHAR(50),
            operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        try:
            await cursor.execute(query)
            return True
        except Exception as e:
            print(f"\033[1;31mError creating table {table_name}: {e}\033[0m")
            return False
    
    # def transactional_with_cursor():
    #     def decorator(func):
    #         @wraps(func)
    #         async def wrapper(*args, **kwargs):
    #             async with MySqlConn.pool.acquire() as conn:
    #                 try:
    #                     if not isinstance(conn, aiomysql.connection.Connection): raise TypeError()
    #                     await conn.begin()
    #                     async with conn.cursor() as cursor:
    #                         result = await func(cursor, *args, **kwargs)
    #                     await conn.commit()
    #                     return result                    
    #                 except Exception as e:
    #                     await conn.rollback()
    #                     print(f"Transaction rolled back due to error: {e}")
    #                     raise
    #         return wrapper
    #     return decorator
   
    # @transactional_with_cursor()
    # async def sqlTransaction(cursor:aiomysql.Cursor, query_list:list):
    #     res_list = []
    #     for query in query_list:
    #         res_list.append(await cursor.execute(query))
    #     return res_list
