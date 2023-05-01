print()
'''
# 字符串操作
abs(x)                  x的绝对值
divmod(x, y)            (x//y, x%y)，输出为二元组形式（也称为元组类型）
pow(x, y[, z])          (x**y)%z，[..]表示该参数可以省略，即：pow(x,y)，它与x**y相同
round(x[, ndigits])     对x四舍五入，保留n digits位小数。round(x)返回四舍五入的整数值
max(x1, x2, …, xn)      x1, x2, …, xn的最大值，n没有限定
min(x1, x2, …, xn)      x1, x2, …, xn的最小值，n没有限定
all(x) 组合类型变量x中所有元素都为真时返回True，否则返回False；若x为空，返回True
any(x) 组合类型变量x中任一元素都为真时返回True，否则返回False；若x为空，返回False
bool(x) 将x转换为Boolean类型，即True或False，bool('') 的结果是False
chr(i) 返回Unicode为i的字符，chr(9996)的结果是'✌ '
complex(r,i) 创建一个复数 r + i*j，complex(10,10)的结果是10+10j
eval(s) 计算字符串s作为Python表达式的值，eval('1+99')的结果是100
exec(s) 计算字符串s作为Python语句的值,exec('a = 1+999')运行后，变量a的值为1000

str.lower()             返回字符串str的副本，全部字符小写
str.upper()             返回字符串str的副本，全部字符大写
str.split(sep=None)     返回一个列表，由str根据sep被分割的部分构成
str.count(sub)          返回sub子串出现的次数
str.replace(old, new)   返回字符串str的副本，所有old子串被替换为new
str.center(width, fillchar) 字符串居中函数，fillchar参数可选
str.strip(chars)        从字符串str中去掉在其左侧和右侧chars中列出的字符
str.join(iter)          将iter变量的每一个元素后增加一个str字符串

Python数据类型转换函数
len(x) 返回字符串x的长度，也可返回其他组合数据类型的元素个数
str(x) 返回任意类型x所对应的字符串形式
chr(x) 返回Unicode编码x对应的单字符
ord(x) 返回单字符x表示的Unicode编码
bin(x) 将整数x转换为等值的二进制字符串 bin(1010)的结果是'0b1111110010'
hex(x) 返回整数x对应十六进制数的小写形式字符串
oct(x) 返回整数x对应八进制数的小写形式字符串
int(x) 将x转换为整数，x可以是浮点数或字符串
float(x) 将x转换为浮点数，x可以是整数或字符串
str(x) 将x转换为字符串，x可以是整数或浮点数
'''
'''字符串操作'''
a = 'helLO'
# 1字母处理：
'''print(a.upper())    # 全部大写
print(a.lower())    # 全部小写
print(a.swapcase()) # 大小写互换
print(a.capitalize())   # 首字母大写，其余小写
print(a.title())    # 首字母大写'''
# 2格式化相关
'''a='1 2'
print(a.ljust(10))  # 获取固定长度，左对齐，右边不够用空格补齐
print(a.rjust(10))  # 获取固定长度，右对齐，左边不够用空格补齐
print(a.center(10)) # 获取固定长度，中间对齐，两边不够用空格补齐
print(a.zfill(10))  # 获取固定长度，右对齐，左边不足用0补齐'''
# 3 字符串搜索相关
s = 'hello world'
'''print(s.find('e'))  # 搜索指定字符串,没有返回-1
print(s.find('w',1,2))  # 顾头不顾尾，找不到则返回-1不会报错，找到了则显示索引
print(s.index('w',1,2)) # 同上，但是找不到会报错
print(s.count('o')) # 统计指定的字符串出现的次数
print(s.rfind('l')) # 从右边开始查找'''

# 4字符串替换
# .replace('old','new')    # 替换old为new
# .replace('old','new',次数)    # 替换指定次数的old为new
s = 'hello world'
'''print(s.replace('world','python'))
print(s.replace('l','p',2))
print(s.replace('l','p',5))'''

# 5字符串去空格及去指定字符
s = ' -h e-ll o- '
# # print(s.strip()) # .strip()    # 去两边空格
# print(s.lstrip()) # .lstrip()    # 去左边空格
# print(s.rstrip()) # .rstrip()    # 去右边空格
# print(s.split('-')) # .split('指定字符')
# print(s.split())    # 按指定字符分割字符串为数组 默认按空格分隔

'''6字符串判断相关
.startswith('start')    # 是否以start开头
.endswith('end')    # 是否以end结尾
.isalnum()    # 是否全为字母或数字
.isalpha()    # 是否全字母
.isdigit()    # 是否全数字
.islower()    # 是否全小写
.isupper()    # 是否全大写
.istitle()    # 判断首字母是否为大写
.isspace()    # 判断字符是否为空格'''

'''#类型转换
bool：根据传入的参数的逻辑值创建一个新的布尔值
bool()
int：根据传入的参数创建一个新的整数
int()  # 不传入参数时，得到结果0
float：根据传入的参数创建一个新的浮点数
float()  # 不提供参数的时候，返回0.0
complex：根据传入参数创建一个新的复数
complex()  # 当两个参数都不提供时，返回复数 0j
str：返回一个对象的字符串表现形式(给用户)
range()    # 函数：可以生成一个整数序列
type()    # 查看数据类型
len()    # 计算字符串长度
format()    # 格式化字符串
ord：返回Unicode字符对应的整数
print(ord('a')) #97
chr：返回整数所对应的Unicode字符
print(chr(97)) #'a'
bin()：将整数转换成2进制字符串
oct()：将整数转化成8进制数字符串
hex()：将整数转换成16进制字符串

tuple：根据传入的参数创建一个新的元组
list：根据传入的参数创建一个新的列表
dict：根据传入的参数创建一个新的字典
set：根据传入的参数创建一个新的集合
# frozenset：根据传入的参数创建一个新的不可变集合
'''
# open() #使用指定的模式和编码打开文件，返回文件读写对象
# 写入文件
# a = open('a.txt', 'w')
# a.write('aking')
# # 读取文件
# a = open('a.txt', 'rt')
# print(a.read())
# a.close()

'''编译执行'''
# compile：将字符串编译为代码或者AST对象，使之能够通过exec语句来执行或者eval进行求值
# 流程语句使用exec
'''
code1 = 'for i in range(5):print(i)'
compile1 = compile(code1, '', 'exec')
exec(compile1)

# 简单求值表达式用eval
code2 = '1+2+3+4'
compile2 = compile(code2, '', 'eval')
print(eval(compile2))  # 10

# eval：执行动态表达式求值
print(eval('1+2+3+4'))  # 10
print(eval('2*2*2'))  # 8
print(eval('10/2+2*2'))  # 9.0

# exec：执行动态语句块
exec('a=1+2')
print(a)  # 3
exec('b=4*3/2-1')
print(b)  # 5.0

# repr：返回一个对象的字符串表现形式(给解释器)
a = 'hello world\n'
print(str(a))  # hello world
print(repr(a))  # 'hello world\n'
'''

'''
文件对象的方法

f.read()
为了读取一个文件的内容，调用 f.read(size), 这将读取一定数目的数据, 然后作为字符串或字节对象返回。
f.write()
f.write(string) 将 string 写入到文件中, 然后返回写入的字符数。
f.tell()
f.tell() 返回文件对象当前所处的位置, 它是从文件开头开始算起的字节数。
f.seek()
如果要改变文件当前的位置, 可以使用 f.seek(offset, from_what) 函数。
from_what 的值, 如果是 0 表示开头, 如果是 1 表示当前位置, 2 表示文件的结尾
f.close()
在文本文件中 (那些打开文件的模式下没有 b 的), 只会相对于文件起始位置进行定位。

pickle 模块
python的pickle模块实现了基本的数据序列和反序列化。通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，永久存储。
通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。
基本接口：pickle.dump(obj, file, [,protocol])
#------------------------------------------------------
参数说明:
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
file: 必需，文件路径（相对或者绝对路径）。
mode: 可选，文件打开模式
buffering: 设置缓冲
encoding: 一般使用utf8
errors: 报错级别
newline: 区分换行符
closefd: 传入的file参数类型
opener:
'''
# 序列类
'''
x in s 如果x是s的元素，返回True，否则返回False
x not in s 如果x不是s的元素，返回True，否则返回False
s + t 连接s和ts * n 或 n * s 将序列s复制n次
s[i] 索引，返回序列的第i个元素
s[i: j] 切片，返回包含序列s第i到j个元素的子序列（不包含第j个元素）
s[i: j: k] 步骤切片，返回包含序列s第i到j个元素以k为步数的子序列
len(s) 序列s的元素个数（长度）
min(s) 序列s中的最小元素
max(s) 序列s中的最大元素
s.index(x) 序列s中第一次出现元素x的位置
s.count(x) 序列s中出现x的总次数
'''

'''
#列表[] list()
len(ls) 列表ls的元素个数（长度）
min(ls) 列表ls中的最小元素
max(ls) 列表ls中的最大元素
list(x) 将x转变成列表类型

ls.append(x) 在列表ls最后增加一个元素x
ls.insert(i, x) 在列表ls第i位置增加元素x
ls.clear() 删除ls中所有元素
ls.pop(i) 将列表ls中第i项元素取出并删除该元素
ls.remove(x) 将列表中出现的第一个元素x删除
ls.reverse() 列表ls中元素反转
ls.copy() 生成一个新列表，复制ls中所有元素

字典 {'':''}
len(d) 字典d的元素个数（长度）
min(d) 字典d中键的最小值
max(d) 字典d中键的最大值
dict() 生成一个空字典
d.keys() 返回所有的键信息
d.values() 返回所有的值信息
d.items() 返回所有的键值对
d.get(key, default) 键存在则返回相应值，否则返回默认值
d.pop(key, default) 键存在则返回相应值，同时删除键值对，否则返回默认值
d.popitem() 随机从字典中取出一个键值对，以元组(key, value)形式返回，取出后从字典中删除这个键值对。
d.clear() 删除所有的键值对
'''

'''
#内置函数
input(s) 获取用户输入，其中s是字符串，作为提示信息s可选
int(x) 将x转换成整数,int(9.9)的结果是9,list(x) 创建或将变量x转换成一个列表类型
list({10,9,8})的结果是[8,9,10]
max(a1,a2,…) 返回参数的最大值
max(1,2,3,4,5)的结果是5min(a1,a2,…) 返回参数的最小值
min(1,2,3,4,5)的结果是1oct(x) 将整数x转换成等值的八进制字符串形式
open(fname, m) 打开文件，包括文本方式和二进制方式等其中，m部分可以省略，默认是以文本可读形式打开
print(x) 打印变量或字符串x,end参数用来表示输出的结尾字符
range(a,b,s) 从a到b(不含)以s为步长产生一个序列list(range(1,10,3))的结果是[1, 4, 7]
reversed(r) 返回组合类型r的逆序迭代形式for i in reversed([1,2,3])将逆序遍历列表
round(n) 四舍五入方式计算n，round(10.6)的结果是11set(x) 将组合数据类型x转换成集合类型
set([1,1,1,1])的结果是{1}
sorted(x) 对组合数据类型x进行排序，默认从小到大sorted([1,3,5,2,4])的结果是[1,2,3,4,5]
str(x) 将x转换为等值的字符串类型str(0x1010)的结果是'4112'
sum(x) 对组合数据类型x计算求和结果sum([1,3,5,2,4])的结果是15
type(x) 返回变量x的数据类型type({1:2})的结果是<class 'dict'>
'''

'''
#turtle
turtle.setup(width, height, startx, starty) 作用：设置主窗体的大小和位置参数：
width ：窗口宽度，如果值是整数，表示的像素值；如果值是小数，表示窗口宽度与屏幕的比例；
height: 窗口高度，如果值是整数，表示的像素值；如果值是小数，表示窗口高度与屏幕的比例；
startx：窗口左侧与屏幕左侧的像素距离，如果值是None，窗口位于屏幕水平中央；
starty：窗口顶部与屏幕顶部的像素距离，如果值是None，窗口位于屏幕垂直中央；

pendown() 放下画笔
penup() 提起画笔，与
pendown()配对使用
pensize(width) 设置画笔线条的粗细为指定大小
color() 设置画笔的颜色
begin_fill() 填充图形前，调用该方法
end_fill() 填充图形结束
filling() 返回填充的状态，True为填充，False为未填充
clear() 清空当前窗口，但不改变当前画笔的位置
reset() 清空当前窗口，并重置位置等状态为默认值
screensize() 设置画布的长和宽
hideturtle() 隐藏画笔的turtle形状
showturtle() 显示画笔的turtle形状
isvisible() 如果turtle可见，则返回True
forward() 沿着当前方向前进指定距离
backward() 沿着当前相反方向后退指定距离
right(angle) 向右旋转angle角度
left(angle) 向左旋转angle角度
goto(x,y) 移动到绝对坐标（x,y）处
setx( ) 将当前x轴移动到指定位置
sety( ) 将当前y轴移动到指定位置
setheading(angle) 设置当前朝向为angle角度
home() 设置当前画笔位置为原点，朝向东。
circle(radius,e) 绘制一个指定半径r和角度e的圆或弧形
dot(r,color) 绘制一个指定半径r和颜色color的圆点
undo() 撤销画笔最后一步动作
speed() 设置画笔的绘制速度，参数为0-10之间
'''

'''
seed(a=None) 初始化随机数种子，默认值为当前系统时间
random() 生成一个[0.0, 1.0)之间的随机小数
randint(a, b) 生成一个[a,b]之间的整数
getrandbits(k) 生成一个k比特长度的随机整数
randrange(start, stop[, step]) 生成一个[start, stop)之间以step为步数的随机整数
uniform(a, b) 生成一个[a, b]之间的随机小数
choice(seq) 从序列类型(例如：列表)中随机返回一个元素
shuffle(seq) 将序列类型中元素随机排列，返回打乱后的序列
sample(pop, k) 从pop类型中随机选取k个元素，以列表类型返回
'''
# import time
# print(time.time())
# print(time.strftime("%Y-%m-%d %H:%M:%S")) #
# print(time.asctime(time.localtime())) #一种时间格式
'''
格式化字符串 日期/时间 值范围和实例
%Y          年份 0001~9999，例如：1900
%m          月份 01~12，例如：10
%B          月名 January~December，例如：April
%b          月名缩写 Jan~Dec，例如：Apr
%d          日期 01 ~ 31，例如：25
%A          星期 Monday~Sunday，例如：Wednesday
%a          星期缩写 Mon~Sun，例如：Wed
%H          小时（24h制） 00 ~ 23，例如：12
%I          小时（12h制） 01 ~ 12，例如：7
%p          上/下午 AM, PM，例如：PM
%M          分钟 00 ~ 59，例如：26
%S          秒 00 ~ 59，例如：26
#-----------------------------------------
import time
def coreLoop():
	limit = 10**8
	while (limit > 0):
		limit -= 1
def otherLoop1():
	time.sleep(0.2)
def otherLoop2():
	time.sleep(0.4)
def main():
	startTime = time.localtime()
	print('程序开始时间：', time.strftime('%Y-%m-%d %H:%M:%S', startTime))
	startPerfCounter = time.perf_counter()
	otherLoop1()
	otherLoop1PerfCounter = time.perf_counter()
	otherLoop1Perf = otherLoop1PerfCounter - startPerfCounter
	coreLoop()
	coreLoopPerfCounter = time.perf_counter()
	coreLoopPerf = coreLoopPerfCounter - otherLoop1PerfCounter
	otherLoop2()
	otherLoop2PerfCounter = time.perf_counter()
	otherLoop2Perf = otherLoop2PerfCounter -
	coreLoopPerfCounter
	endPerfCounter = time.perf_counter()
	totalPerf = endPerfCounter - startPerfCounter
	endTime = time.localtime()
	print("模块1运行时间是:{}秒".format(otherLoop1Perf))
	print("核心模块运行时间是:{}秒".format(coreLoopPerf))
	print("模块2运行时间是:{}秒".format(otherLoop2Perf))
	print("程序运行总时间是:{}秒".format(totalPerf))
	print('程序结束时间：', time.strftime('%Y-%m-%d %H:%M:%S', endTime))
main()
'''
# 第三方库
'''
PyInstaller
是一个十分有用的Python第三方库，它能够将Python源文件打包，变成直接可运行的可执行文件。
PyInstaller -F SnowView.py

jieba
jieba库的分词原理是利用一个中文词库，将待分词的内容与分词词库进行比对，通过图结构和动态规划方法找到最大概率的词组。
除了分词，jieba还提供增加自定义中文单词的功能
jieba库支持三种分词模式：
1.精确模式，将句子最精确地切开，适合文本分析；
jieba.lcut(s)即将字符串分割成等量的中文词组，返回结果是列表类型
2.全模式，把句子中所有可以成词的词语都扫描出来，速度非常快，但是不能解决歧义；
jieba.lcut(s, cut_all = True)将字符串的所有分词可能均列出来，返回结果是列表类型，冗余性最大
3.搜索引擎模式，在精确模式基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
jieba.lcut_for_search(s)首先执行精确模式，然后再对其中长词进一步切分获得最终结果
'''
'''
wordcloud
词云以词语为基本单元，根据其在文本中出现的频率设计不同大小以形成视觉上不同效果，
形成“关键词云层”或“关键词渲染”，从而使读者只要“一瞥”即可领略文本的主旨。

爬虫方向
requests
requests库是一个简洁且简单的处理HTTP请求的第三方库，它的最大优点是程序编写过程更接近正常URL访问过程。
这个库建立在Python语言的urllib3库基础上。request库支持非常丰富的链接访问功能。
scrapy
scrapy是Python开发的一个快速的、高层次的Web获取框架。不同于简单的网络爬虫功能，scrapy框架本身包含了
成熟网络爬虫系统所应该具有的部分共用功能，scrapy用途广泛，可以应用于专业爬虫系统的构建、数据挖掘、网络监控和自动化测试等领域

数据分析方向
numpy
numpy是Python的一种开源数值计算扩展第三方库，用于处理数据类型相同的多维数组（ndarray），简称“数组”。
这个库可用来存储和处理大型矩阵，比Python语言提供的列表结构要高效的多。numpy提供了许多高级的数值编程工具，如：矩阵运算、矢量处理、N维数据变换等
scipy
scipy是一款方便、易于使用、专为科学和工程设计的# Python工具包。在numpy库的基础上增加了众多的数学、科学以及工程计算中常用的库函数。
它包括统计、优化、整合、线性代数、傅里叶变换、信号分析、图像处理、常微分方程求解等众多模块
pandas
pandas是基于numpy扩展的一个重要第三方库，它是为# 了解决数据分析任务而创建的。Pandas提供了一批标准的数据模型和大量
快速便捷处理数据的函数和方法，提供了高效地操作大型数据集所需的工具。提供两种最基本的数据类型：Series和DataFrame，分别代表一维数组和二维数组类型

文本处理
pdfminer
pdfminer是一个可以从PDF文档中提取各类信# 息的第三方库。
Pdfminer能够获取PDF中文本的准确位置、字体、行数等信息，能够将PDF文件转换为HTML及文本格式
pdfminer
pdfminer包含两个重要的工具：pdf2txt.py和dumppdf.py。pdf2txt.py能够从PDF文件中提取所有文本内容。
dumppdf.py能够把PDF文件内容变成XML格式，并进一步提取其中的图片
openpyxl
openpyxl是一个处理Microsoft Excel文档的Python第三方库，它支持读写Excel的xls、xlsx、xlsm、xltx、xltm等格式文件，
并进一步能处理Excel文件中excel工作表、表单和数据单元
python-docx
python-docx是一个处理Microsoft Word文档的Python第三方库，它支持读取、查询以及修改doc、docx等格式文件，
并能够对Word常见样式进行编程设置，包括：字符样式、段落样式、表格样式等，进一步可以使用这个库实现添加和修改文本、图像、样式和文档等功能
beautifulsoup4
beautifulsoup4库，也称为Beautiful Soup库或bs4库，用于解析和处理HTML和XML。需要注意，它不是BeautifulSoup库。
它的最大优点是能根据HTML和XML语法建立解析树，进而高效解析其中的内容beautifulsoup4库将数据从HTML和XML文件中解析出来，
它能够提供一种符合习惯的方法去遍历搜索和修改解析树，将专业的Web页面格式解析部分封装成函数，提供了若干有用且便捷的处理函数

'''
# print('{:.3f}'.format(((3**4+5*6**7)/8)**0.5))
# print("二进制{0:b}、十进制{0:d}、八进制{0:o}、十六进制{0:x}".format(0x4DC0+50))

import turtle
# d = 0
# for i in range(4):
#     turtle.fd(200)
#     d = d+90
#     turtle.seth(d)
def main0():
    ls = ["综合", "理工", "综合", "综合", "综合", "综合", "综合", "综合", "综合", "综合", \
          "师范", "理工", "综合", "理工", "综合", "综合", "综合", "综合", "综合", "理工", \
          "理工", "理工", "理工", "师范", "综合", "农林", "理工", "综合", "理工", "理工", \
          "理工", "综合", "理工", "综合", "综合", "理工", "农林", "民族", "军事"]

    dict = {}
    for i in ls:
        dict[i] = dict.get(i, 0) + 1  #统计字典
    # print(dict)
    list0 = list(dict.items()) #转列表
    # print(tlist)
    list0.sort(key=lambda x: x[1],reverse=True) #以排序

    for i in range(len(dict)):
        name, count = list0[i] #列表拆分
        print('{0}:{1}'.format(name, i+1)) #以输出 count
main0()
'''    d = {}
    for word in ls:
        d[word] = d.get(word, 0) + 1
    for k in d:
        print("{}:{}".format(k, d[k])) #字典默认排序吗'''
# ------------------------------------------------------
# print(3**0.5*pow(3,0.5)==3)
#
# for i in range(12):
#     print(chr(ord("♈")+i),end="")


def main1():
    fin = open("论语-网络版.txt", "r", encoding="utf-8")
    fout = open("论语-提取版.txt", "w")
    wflag = False            #写标记
    for line in fin:
        # print(line)
        if "【" in line:     #遇到【时，说明已经到了新的区域，写标记置否。  将原文标记删除
            wflag = False
        if "【原文】" in line:  #遇到【原文】时，设置写标记为True
            wflag = True
            continue #跳过下面的操作，既不显示 【原文】
        if wflag == True:    #根据写标记将当前行内容写入新的文件
            # for i in range(0,10):
            #     for j in range(0,10):
            #         line = line.replace("{}·{}".format(i,j),"") #删除文中 'i·j' 字符，数字章节字符
            # for i in range(0,10):
            #     line = line.replace("*{}".format(i),"")
            # for i in range(0,10):
            #     line = line.replace("{}*".format(i),"")

            fout.write(line)
    fin.close()
    fout.close()
# main()
# -----------------------------
def main2():
# if __name__=='__main__':
    fi = open("论语-提取版.txt", "r")
    fo = open("论语-原文.txt", "w")
    for line in fi:   #逐行遍历
        for i in range(1,23):  #对产生1到22数字
            line=line.replace("({})".format(i), "")  #构造(i)并替换 ; (i)不可行
        fo.write(line)
    fi.close()
    fo.close()
# main()
def main3():
    fi = open("论语-网络版.txt", "r", encoding='utf-8')
    fo = open("论语-字符统计.txt", "w", encoding='utf-8')
    txt = fi.read()
    d = {}
    for c in txt: #不用 jieba.lcut(txt) 默认单个字符分割
        d[c] = d.get(c, 0) + 1
    del d[' ']
    del d['\n']
    list0=list(d.items()) #    print(list0)
    ls = []
    for key in d:
        ls.append("{}:{}".format(key, d[key]))
    # print(ls)
    fo.write("  ".join(ls)) # join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串。
    fi.close()
    fo.close()
# main()

print('hello')
