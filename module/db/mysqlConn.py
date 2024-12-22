import aiomysql
from functools import wraps


class MySqlConn:
    mysqlConnDict:dict[str, aiomysql.pool.Pool] = {}
    nowDbName:str = None

    async def openConn(host:str, port:int, user:str, password:str, db_name:str):
        try:
            pool = await aiomysql.create_pool(host = host, port = port, user = user,
                                              password = password, db = db_name)
            MySqlConn.mysqlConnDict[db_name] = pool
            print(f"\033[1;32mMysql database {db_name} connection opened.\033[0m")
            print(f"\033[1;30m", end='')
            print(f"  -- host:    {host}")
            print(f"  -- port:    {port}")
            print(f"  -- user:    {user}")
            print(f"  -- db:      {db_name}")
            print("\033[0m")
        except Exception as e:
            print(f"\033[1;31mError occurred while openConn:\033[0m {e}")


    async def closeConn(db_name:str):
        try:
            db:aiomysql.pool.Pool = MySqlConn.mysqlConnDict.pop(db_name)
        except Exception:
            return print(f"\033[1;31mMysql database {db_name} is not connected.\033[0m")
        db.close()
        print("db.close...")
        await db.wait_closed()
        print(f"\033[1;33mMysql database `{db_name}` connection closed.\033[0m")
    

    def useDb(db_name:str):
        if db_name not in MySqlConn.mysqlConnDict.keys():
            return print(f"\033[1;31mMysql database {db_name} is not connected.\033[0m")
        MySqlConn.nowDbName = db_name
    
    
    def with_cursor():
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                async with MySqlConn.mysqlConnDict[MySqlConn.nowDbName].acquire() as conn:
                    if not isinstance(conn, aiomysql.connection.Connection): raise TypeError()
                    async with conn.cursor() as cursor:
                        res = await func(cursor, *args, **kwargs)
                        await conn.commit()
                return res
            return wrapper
        return decorator


    @with_cursor()
    async def rawSqlCmd(cursor:aiomysql.cursors.Cursor, query:str):
        try:
            n = await cursor.execute(query)
        except Exception as e:
            return print(f"\033[1;31mError occurred when execute query `{query}`. {e}.\033[0m")
        return await cursor.fetchall()
    
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