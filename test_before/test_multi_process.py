
from multiprocessing import Process, Pipe
import time
import sys
import os

# from send_msg import send_message


def send_message(conn):  # 发送message
    print('send_message id: ', os.getpid())
    for i in range(1000):
        print('send_message:%d' % i)
        conn.send(i)
        time.sleep(2)


def recv_message(conn):  # 接受message
    # for i in range(1000):
    # print('recv_message: ', conn.recv())
    while True:
        if conn.recv() % 5 == 0:
            print('recv_message: 5%')
        time.sleep(1)


if __name__ == '__main__':
    # 创建一个进程通信管道
    left, right = Pipe()
    t1 = Process(target=send_message, args=(left,))
    t2 = Process(target=recv_message, args=(right,))

    t1.start()
    t2.start()
