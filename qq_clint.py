from socket import *
from multiprocessing import *
import sys

ADDR = ("127.0.0.1",6666)

def login(sock):
    while True:
        name = input("Name:")
        msg = "L "+name
        sock.sendto(msg.encode(),ADDR)
        result,addr = sock.recvfrom(128)
        if result.decode() == "OK":
            print("进入聊天室！")
            return name
        else:
            print("该用户已存在！")

def recv_msg(sock):
    while True:
        data,addr=sock.recvfrom(1024*10)
        msg = "\n"+data.decode()+"\n发言:"
        print(msg,end="")

def send_msg(sock,name):
    while True:
        try:
            content = input("发言:")
        except KeyboardInterrupt:
            content = "exit"
        if content == "exit":
            msg = "E "+name
            sock.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室！")
        msg = "C %s %s"%(name,content)
        sock.sendto(msg.encode(),ADDR)

def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    # sock.bind(("0.0.0.0",27116))

    name = login(sock)

    p = Process(target=recv_msg,args=(sock,))
    p.daemon = True
    p.start()
    send_msg(sock,name)

if __name__ == '__main__':
    main()
