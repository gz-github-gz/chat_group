from select import *
from socket import *
import re


class WebServer:
    def __init__(self, host="0.0.0.0", port=8000, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.create_socket()
        self.bind()
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sock.bind(self.address)

    def start(self):
        self.sock.listen(5)
        print("Listen the port of %d" % self.port)
        self.rlist.append(self.sock)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sock:
                    connfd, addr = r.accept()
                    print("Connect from", addr)
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    self.handle(r)

    # def handle(self, connfd):
    #     request = connfd.recv(1024 * 10).decode()
    #     pattern = "[A-Z]+\s+(?P<info>/\s*)"
    #     result = re.match(pattern, request)
    #     if result:
    #         info = result.group("info")
    #         print("请求内容:", info)
    #         self.send_html(connfd, info)
    #         print("3==============")
    #     else:
    #         connfd.close()
    #         self.rlist.remove(connfd)
    #         return
    def handle(self, connfd):
        # 接受浏览器请求
        request = connfd.recv(1024 * 10).decode()
        # 解析请求 --> 获取请求内容
        pattern = "[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, request)
        if result:
            # 匹配到了内容 --> 请求内容
            info = result.group('info')
            print("请求内容:", info)
            # 发送响应数据
            self.send_html(connfd, info)
        else:
            # 没有匹配到,认为客户端断开
            connfd.close()
            self.rlist.remove(connfd)
            return

    def send_html(self, connfd, info):
        if info == "/":
            print(1)
            filename = self.html + "/index.html"
            print(filename)
        else:
            filename = self.html + info
        try:
            f = open(filename, "rb")
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Connect-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry...</h1>"
            response = response.encode()
        else:
            data = f.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Connect-Type:text/html\r\n"
            response += "Connect-Length:%d\r\n" % len(data)
            response += "\r\n"
            response = response.encode() + data
        finally:
            connfd.send(response)


if __name__ == '__main__':
    httpd = WebServer(host="0.0.0.0", port=8885, html="/home/tarena/month02/day17/static")
    httpd.start()
