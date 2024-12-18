import sys

import aiomysql
import pymysql
from functools import wraps


class MySqlConn:
    pool:aiomysql.pool.Pool = None
    host:str = "127.0.0.1"
    port:int = 3306
    user:str = "root"
    password:str = "FORever1437"
    db:str = "lvrulan_mysql"

    def __init__(self, host:str, port:int, user:str, password:str, db:str):
        MySqlConn.host = host
        MySqlConn.port = port
        MySqlConn.user = user
        MySqlConn.password = password
        MySqlConn.db = db


    async def openConn(*args, **kwargs):
        MySqlConn.pool = await aiomysql.create_pool(
            host = MySqlConn.host,
            port = MySqlConn.port,
            user = MySqlConn.user,
            password = MySqlConn.password,
            db = MySqlConn.db,
        )

        print(f"\033[1;32mMysql database connection opened.")
        print(f"\033[1;30m", end='')
        print(f"  -- host:    {MySqlConn.host}")
        print(f"  -- port:    {MySqlConn.port}")
        print(f"  -- user:    {MySqlConn.user}")
        print(f"  -- db:      {MySqlConn.db}")
        print("\033[0m")


    async def closeConn(*args, **kwargs):
        MySqlConn.pool.close()
        await MySqlConn.pool.wait_closed()
        print("\033[1;33mMysql database connection closed.")
        print("\033[0m")
    
    
    def with_cursor():
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                async with MySqlConn.pool.acquire() as conn:
                    if not isinstance(conn, aiomysql.connection.Connection): raise TypeError()
                    async with conn.cursor() as cursor:
                        res = await func(cursor, *args, **kwargs)
                        await conn.commit()
                return res
            return wrapper
        return decorator

    
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
    
    @with_cursor()
    async def rawSqlCmd(cursor:aiomysql.Cursor, query:str):
        try:
            n = await cursor.execute(query) # n 为该操作影响的行数
        except pymysql.err.ProgrammingError:
            exc_type, exc_value, exc_tb = sys.exc_info()
            err_code, err_msg = exc_value.args
            exc_class = f"{exc_type.__module__}.{exc_type.__name__}"

            print("\033[1;31m", end='', file=sys.stderr)
            print(f"{exc_class} occurred in `{__file__}` at line {exc_tb.tb_lineno}.", file=sys.stderr)
            print("\033[1;30m", end='', file=sys.stderr)
            print(f"  -- Error Code:      {err_code}", file=sys.stderr)
            print(f"  -- Error Message:   {err_msg}", file=sys.stderr)
            print("\033[0m", end='', file=sys.stderr)
            return None
        return await cursor.fetchall()
    
    
    # @transactional_with_cursor()
    # async def sqlTransaction(cursor:aiomysql.Cursor, query_list:list):
    #     res_list = []
    #     for query in query_list:
    #         res_list.append(await cursor.execute(query))
    #     return res_list