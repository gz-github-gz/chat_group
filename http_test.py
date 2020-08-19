"""
http 请求响应演示
"""
from socket import *


s = socket()
s.bind(("0.0.0.0",8888))
s.listen(5)


c,addr = s.accept()
data = c.recv(1024*10)
print(data.decode())

html = "HTTP/1.1 200 OK\r\n"
html +="Content_Type:text/html\r\n"
html +="\r\n"
with open("/home/tarena/month02/day17/超文本_百度百科.html") as f:
    html += f.read()

c.send(html.encode())

c.close()
s.close()

# 127.0.0.1:8888