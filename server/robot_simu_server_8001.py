#!/usr/bin/env python3
"""
松下PLC TCP测试服务器 - 回显+机械臂状态模拟
"""

import socket
import time

def echo_server():
    """回显服务器"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8001))
    sock.listen(1)

    print("松下PLC TCP回显服务器")
    print("端口: 8001")
    print("等待PLC连接...")
    print("-" * 50)

    arm_busy_until = 0  # 机械臂忙状态截止时间（时间戳）

    try:
        while True:
            conn, addr = sock.accept()
            print(f"\n[+] PLC连接: {addr[0]}:{addr[1]}")

            with conn:
                conn.settimeout(60)  # 60秒无数据超时

                while True:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            print(f"[-] PLC断开")
                            break

                        # 尝试解析文本
                        text = data.decode('ascii', errors='ignore').strip()
                        if text:
                            print(f"接收指令: {text[:50]}", end="")
                            if len(text) > 50:
                                print("...")
                            else:
                                print()
                        print(f"时间: {time.strftime('%H:%M:%S')}")
                        print("-" * 30)

                        # 检查指令
                        now = time.time()
                        if 'MOVE' in text.upper():
                            arm_busy_until = now + 3  # 机械臂忙3秒
                            conn.sendall(b'OK')
                            print("[📤 响应] MOVE -> OK")
                        elif 'GET STATUS' in text.upper():
                            if now < arm_busy_until:
                                conn.sendall(b'BUSY')
                                print("[📤 响应] GET STATUS -> BUSY")
                            else:
                                conn.sendall(b'IDLE')
                                print("[📤 响应] GET STATUS -> IDLE")
                        else:
                            # 回显其他数据
                            conn.sendall(data)
                            print(f"[📤 响应] 已回显 {len(data)} 字节")

                    except socket.timeout:
                        print(f"\n[!] 60秒无数据，等待新连接...")
                        break
                    except ConnectionResetError:
                        print(f"\n[!] PLC强制断开连接")
                        break
                    except Exception as e:
                        print(f"\n[!] 错误: {e}")
                        break

    except KeyboardInterrupt:
        print("\n\n服务器关闭")
    finally:
        sock.close()


if __name__ == "__main__":
    echo_server()
