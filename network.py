import socket
import threading
import time
import numpy as np
import xgboost as xgb


def get_data(sock):
    try:
        data = sock.recv(4096)
        data = data.decode('utf-8')
        return data
    except Exception as e:
        print(e)
        return 'quit'


lock = threading.Lock()
def use_msg(msg):
    lock.acquire()
    if len(msg) == 0:
        return
    print("msg = ", msg)
    lock.release()


# 处理客户端，sock为socket，addr为客户端地址
def tcp_server(sock, addr):
    print("Accept new connection from %s:%s" % addr)
    while True:
        data = get_data(sock)
        use_msg(data)
    sock.close()
    print('Connection from %s:%s closed.' % addr)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 3288))
    sock.listen(100)
    print("TCP Server is running")
    print("Wait for new Connection")
    while True:
        sock_fd, addr = sock.accept()
        thread = threading.Thread(target=tcp_server, args=(sock_fd, addr))
        thread.start()
