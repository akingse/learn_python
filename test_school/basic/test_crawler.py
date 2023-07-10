print()
'''
#爬虫测试
# -*- coding:UTF-8 -*-
import requests
if __name__ == '__main__':
    target = 'http://www.mi.com/'
    req = requests.get(url=target)
    req.encoding = 'GBK'  #'utf-8'
    #print(req.text)
'''
'''
# if __name__ == '__main__':
#     target = 'http://www.biqukan.com/1_1094/5403177.html'
#     req = requests.get(url=target)
#     req.encoding = 'GBK' #获取的编码不是GBK，而是ISO-8859-1，需要将编码改为GBK
    #print(req.text)


from bs4 import BeautifulSoup
import requests
if __name__ == "__main__":
     target = 'http://www.biqukan.com/1_1094/5403177.html'
     req = requests.get(url = target)
     req.encoding = 'GBK'
     html = req.text
     bf = BeautifulSoup(html)
     texts = bf.find_all('div', class_ = 'showtxt')
     print(texts)
     print(texts[0].text.replace('\xa0'*8,'\n\n'))
'''
'''
#coding:utf-8
#import urllib
#import numpy as np
#版本不和，python2->python3各种错误

import urllib.request
from urllib import request
import re

def get_html(url):
    page = request.urlopen(url)
    html_code = page.read()
    return html_code

def get_image(html_code):
    reg = r'src="(.+?\.jpg)" width'
    reg_img = re.compile(reg)
    img_list = reg_img.findall(html_code)
    x = 0
    for img in img_list:
        #request.urlretrieve(img, '%s.jpg' % x)
        request.urlretrieve(img, 'd:/py/img/%s.jpg' % x)
        x += 1

print('-------网页图片抓取-------')
print('请输入url:')
url = input()
'''
'''
if url:
    pass
else:
    print('---没有地址输入正在使用默认地址---')
    url = 'http://tieba.baidu.com/p/1753935195'

print('----------正在获取网页---------')
html_code = get_html(url)
print('----------正在下载图片---------')
get_image(html_code)
print('-----------下载成功-----------')
print('Press Enter to exit')

#http://tieba.baidu.com/p/1753935195
#https://tieba.baidu.com/p/3045959055
'''
'''
#!/usr/bin/python
#coding:utf-8
import urllib.request

import itertools
def download(url,user_agent='wswp',num_reload=5):
    headers={'User-agent':user_agent}
    request=urllib.request.Request(url,headers=headers)

    #page = request.urlopen(url)
    try:
        html=request.urlopen(request).read()
    except urllib.URLError as e:
        print ('Downloading error:',e.reason)
        html = None
        if num_reload>0 and ( hasattr(e,'code') and 500<=e.code<=600 ):
            return download(url,user_agent,num_reload-1)
    return html

for page in itertools.count(1):
    url='http://example.webscraping.com/view/%d'%page
    html=download(url)
    print (url)
    if html is None:
        break
'''
'''
import urllib.request
import urllib.parse

url = 'http://127.0.0.1:8000/api/login/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
headers['Host'] = 'httpbin.org'
dict = {'user': 'admin', 'pwd': '12345', }

data = urllib.parse.urlencode(dict).encode('utf-8')
# data参数如果要传必须传bytes（字节流）类型的，如果是一个字典，先用urllib.parse.urlencode()编码。
request = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
response = urllib.request.urlopen(request)
html = response.read().decode('utf-8')

print(html)
'''
'''
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys

class downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        #self.target = 'http://www.biqukan.com/1_1094/'
        self.target = 'https://www.biqukan.com/28_28134/'
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = 0  # 章节数

    def get_download_url(self):
        req = requests.get(url=self.target)
        req.encoding = 'GBK'
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])  # 剔除不必要的章节，并统计章节数
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2017-09-13
    """

    def get_contents(self, target):
        req = requests.get(url=target)
        req.encoding = 'GBK'
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2017-09-13
    """

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('《一年永恒》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '一念永恒.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" % float(i / dl.nums) + '\r')
        sys.stdout.flush()
    print('《一年永恒》下载完成')
'''
'''
# https://zhuanlan.zhihu.com/p/68968768
# -*- coding:UTF-8 -*-
import requests
if __name__ == '__main__':
     target = 'https://zhuanlan.zhihu.com/p/68968768'
     req = requests.get(url=target)
     print(req.text)
'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 通过urllib(2)模块下载网络内容
import urllib, urllib2, gevent
# 引入正则表达式模块，时间模块
import re, time
from gevent import monkey

monkey.patch_all()


def geturllist(url):
    url_list = []
    print
    url
    s = urllib2.urlopen(url)
    text = s.read()
    # 正则匹配，匹配其中的图片
    html = re.search(r'<ol.*</ol>', text, re.S)
    urls = re.finditer(r'<p><img src="(.+?)jpg" /></p>', html.group(), re.I)
    for i in urls:
        url = i.group(1).strip() + str("jpg")
        url_list.append(url)
    return url_list


def download(down_url):
    name = str(time.time())[:-3] + "_" + re.sub('.+?/', '', down_url)
    print
    name
    urllib.urlretrieve(down_url, "D:\\TEMP\\" + name)


def getpageurl():
    page_list = []
    # 进行列表页循环
    for page in range(1, 700):
        url = "http://jandan.net/zoo" + str(page) + "#comments" #http://jandan.net/ooxx/page-
        # 把生成的url加入到page_list中
        page_list.append(url)
    print
    page_list
    return page_list

def main():
# if __name__ == '__main__':
    jobs = []
    pageurl = getpageurl()[::-1]
    # 进行图片下载
    for i in pageurl:
        for (downurl) in geturllist(i):
            jobs.append(gevent.spawn(download, downurl))
    gevent.joinall(jobs)