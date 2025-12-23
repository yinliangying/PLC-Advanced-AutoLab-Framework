#!/usr/bin/env python3
"""
松下 PLC TCP 日志服务器
- 适合实时日志
- 简单实现
"""

import socket
import logging

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('plc_tcp_log.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

TCP_IP = "0.0.0.0"
TCP_PORT = 8000
BUFFER_SIZE = 2048


def tcp_log_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(5)  # 同时允许最多5个连接

    logging.info("松下 PLC TCP 日志服务器启动")
    logging.info(f"监听端口: {TCP_PORT}")

    try:
        while True:
            conn, addr = sock.accept()
            logging.info(f"新连接: {addr[0]}:{addr[1]}")
            with conn:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    text = data.decode('utf-8', errors='ignore').strip()
                    if text:
                        logging.info(f"[{addr[0]}:{addr[1]}] {text}")

            logging.info(f"断开连接: {addr[0]}:{addr[1]}")
    except KeyboardInterrupt:
        logging.info("服务器退出")
    finally:
        sock.close()


if __name__ == "__main__":
    tcp_log_server()
