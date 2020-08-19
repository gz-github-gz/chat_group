from socket import *
from multiprocessing import Process

HOST = "0.0.0.0"
PORT = 6666
ADDR = (HOST, PORT)

user = {}

def login(sock, name, addr):
    if name in user:
        sock.sendto(b"FAIL", addr)
        return
    sock.sendto(b"OK", addr)
    msg = "欢迎　%s 进入聊天室" %name
    for i in user:
        sock.sendto(msg.encode(), user[i])
    user[name] = addr

def chat(sock, name, content):
    msg = "%s : %s" % (name, content)
    for i in user:
        if i == name:
            continue
        sock.sendto(msg.encode(), user[i])

def exit(sock,name):
    del user[name]
    msg = "%s 退出聊天室" %name
    for i in user:
        sock.sendto(msg.encode(), user[i])

def request(sock):
    while True:
        data, addr = sock.recvfrom(1024 * 10)
        tmp = data.decode().split(" ", 2)
        if tmp[0] == "L":
            login(sock, tmp[1], addr)
        elif tmp[0] == "C":
            chat(sock, tmp[1], tmp[2])
        elif tmp[0] == "E":
            exit(sock, tmp[1])

def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)

    p = Process(target=request,args=(sock,))
    p.daemon = True
    p.start()
    while True:
        content = input("管理员消息:")
        if content == "exit":
            break
        msg = "C 管理员消息 "+content
        sock.sendto(msg.encode(),ADDR)



if __name__ == '__main__':
    main()
