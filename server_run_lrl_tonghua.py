# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True  # 禁止生成 "__pycache__" 文件夹

import asyncio
import signal
from asyncio import Event
from module.webServer import WebServer

# 配置服务主机和端口
HOST = "0.0.0.0"
PORT = 7500

# 用于触发关闭事件的异步事件
shutdown_event = Event()

# 主程序逻辑
async def main():
    server = WebServer(HOST, PORT)
    asyncio.create_task(server.start())  # 启动 WebServer

    print("Server is running. Waiting for shutdown signal...")
    await shutdown_event.wait()  # 等待关闭信号
    print("Shutting down server...")
    await server.shutdown()  # 优雅关闭服务

# 处理 SIGTERM 信号
def handle_sigterm():
    print("\nSIGTERM received!\nGracefully shutting down...")
    shutdown_event.set()

import platform
import asyncio

# 设置事件循环
if platform.system() == 'Windows':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

# 绑定信号处理器
if platform.system() == 'Windows':
    signal.signal(signal.SIGINT, lambda signum, frame: handle_sigterm())
else:
    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)  # 绑定 SIGTERM 信号

try:
    loop.run_until_complete(main())  # 启动事件循环并运行主程序
except asyncio.CancelledError:
    pass
finally:
    loop.close()  # 关闭事件循环
    print("Program terminated.")
