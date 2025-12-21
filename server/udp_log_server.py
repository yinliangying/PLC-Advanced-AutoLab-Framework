#!/usr/bin/env python3
"""
松下 PLC UDP 日志服务器
- 无连接
- 高吞吐
- 适合实时日志
"""

import socket
import logging
from datetime import datetime

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('plc_udp_log.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

UDP_IP = "0.0.0.0"
UDP_PORT = 8002
BUFFER_SIZE = 2048


def udp_log_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    logging.info("松下 PLC UDP 日志服务器启动")
    logging.info(f"监听端口: {UDP_PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)

            text = data.decode('utf-8', errors='ignore').strip()
            if text:
                logging.info(f"[{addr[0]}:{addr[1]}] {text}")

        except KeyboardInterrupt:
            logging.info("服务器退出")
            break
        except Exception as e:
            logging.error(f"错误: {e}")

    sock.close()


if __name__ == "__main__":
    udp_log_server()
