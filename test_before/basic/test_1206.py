import pprint  # pprint用于输出一个整齐美观Python数据的结构
import socket  # 导入socket库:
import ssl
import numpy as np
x = np.arange(5, 0, -1)
print(x)
y = x[np.array([True, False, True, False, False])]
print(y)

'''
为了把全世界的所有不同类型的计算机都连接起来，就必须规定一套全球通用的协议。
互联网协议包含了上百种协议标准，但是最重要的两个协议是TCP和IP协议，所以，大家把互联网的协议简称TCP/IP协议。
IP协议负责把数据从一台计算机通过网络发送到另一台计算机。
TCP协议则是建立在IP协议之上的。TCP协议负责在两台计算机之间建立可靠连接，保证数据包按顺序到达。
许多常用的更高级的协议都是建立在TCP协议基础上的，比如用于浏览器的HTTP协议、发送邮件的SMTP协议等。
一个TCP报文除了包含要传输的数据外，还包含源IP地址和目标IP地址，源端口和目标端口。每个网络程序都向操作系统申请唯一的端口号。

Socket是网络编程的一个抽象概念。通常我们用一个Socket表示“打开了一个网络链接”，
而打开一个Socket需要知道目标计算机的IP地址和端口号，再指定协议类型即可。
大多数连接都是可靠的TCP连接。创建TCP连接时，主动发起连接的叫客户端，被动响应连接的叫服务器。
'''
'''
JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式。包含不同的数据类型
“名称/值”对的集合（A collection of name/value pairs）。
不同的语言中，它被理解为对象（object），纪录（record），结构（struct），字典（dictionary），哈希表（hash table），有键列表（keyed list），或者关联数组 （associative array）。
值的有序列表（An ordered list of values）。在大部分语言中，它被理解为数组（array）。

'''
def main0():
    '''客户端'''
    # 创建一个socket:
    # AF_INET指定使用IPv4协议，SOCK_STREAM指定使用面向流的TCP协议
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 建立连接:
    s.connect(('www.sina.com.cn', 80))  # 80端口是Web服务的标准端口。
    # 例如SMTP服务是25端口，FTP服务是21端口，等等。端口号小于1024的是Internet标准服务的端口，端口号大于1024的，可以任意使用。
    # 发送数据:
    # 发送的文本格式必须符合HTTP标准
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
    # 接收数据:
    buffer = []
    while True:
        d = s.recv(1024)  # 每次最多接收1k字节:
        if d:
            buffer.append(d)
        else:
            break
    # print(buffer)
    data = b''.join(buffer)  # str.join(sequence) #用str将sequence连接起来
    # print('data =', data)
    # b'HTTP/1.1 302 Moved Temporarily\r\nServer: nginx\r\nDate: Fri, 25 Oct 2019 08:42:57 GMT\r\n
    # Content-Type: text/html\r\nContent-Length: 154\r\nConnection: close\r\nLocation: https://www.sina.com.cn/\r\n
    # X-Via-CDN: f=edge,s=cnc.yizhuang.ha2ts4.93.nb.sinaedge.com,c=117.136.38.143;\r\nX-Via-Edge: 15719929777808f2688755d3810ac7b2f979f\r\n\r\n
    #
    # <html>\r\n<head><title>302 Found</title></head>\r\n<body bgcolor="white">\r\n<center><h1>302 Found</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'

    # s.close()# 关闭连接:
    header, html = data.split(b'\r\n\r\n', 1) #.split('str',1) 分割依据，分割次数；
    print(header.decode('utf-8'))
    print(html.decode('utf-8'))
    # 把接收的数据写入文件:
    with open('sina.html', 'wb') as f:
        f.write(html)  # 302 Found
#新浪强制HTTPS协议访问 所以 80端口改443 socket 改 ssl
def main1():
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(socket.socket())
    s.connect(('www.sina.com.cn', 443))
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

    buffer = []
    d = s.recv(1024)
    while d:
        buffer.append(d)
        d = s.recv(1024)
    data = b''.join(buffer)

    s.close()

    header, html = data.split(b'\r\n\r\n', 1)
    print(header.decode('utf-8'))

    with open('sina.html', 'wb') as f:
        f.write(html)
main0()

'''服务器'''
#服务器进程首先要绑定一个端口并监听来自其他客户端的连接。
#一个Socket依赖4项：服务器地址、服务器端口、客户端地址、客户端端口来唯一确定一个Socket。
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #一个基于IPv4和TCP协议的Socket

