import pprint  # pprint用于输出一个整齐美观Python数据的结构
import socket  # 导入socket库:
import ssl
print(' ')
'''
Python 的解释器
CPython。CPython用>>>作为提示符。这个解释器是用C语言开发的，CPython是使用最广的Python解释器。
IPython用In [序号]:作为提示符。基于CPython之上的一个交互式解释器，IPython只是在交互方式上有所增强
Jython是运行在Java平台上的Python解释器，可以直接把Python代码编译成Java字节码执行。

Autopep8
PEP是 Python Enhancement Proposal 的缩写.PEP8 ，简单说就是一种编码规范，是为了让代码更容易被阅读。
安装：pip install autopep8
使用：autopep8 --in-place --aggressive demo.py
类的函数称为方法（method），模块里的函数称为函数（function）

类型注解
Python是一种动态语言，变量和函数的参数是不区分类型的。
一般变量和函数参数注解格式为“参数：类型”，默认参数是在类型的后面加“=默认值”，
函数的返回值注解格式为“-> 类型:”，函数的冒号在注解后方。
#def list_to_str(param_list: list, connect_str: str=" ") -> str:

反射
计算机中的反射，是在运行的时候来自我检查，并对内部成员进行操作。就是说这个变量的类型可以动态的改变，在运行的时候确定它的作用。
在Python中，能够通过一个对象，找出其type、class、attribute或method的能力，称为反射或自省。
具有反射能力的函数有type(),isinstance(),callable().dir().getattr()等

 Python 的魔法方法
__new__是用来创建类并返回这个类的实例,
__init__将传入的参数来初始化该实例，以及初始化示例属性，与__new__共同构成了“构造函数”
__del__将实例化后的对象销毁，即为析构函数

linux下，像.exe文件那样直接运行.py文件
首行加一个特殊的注释，#!/usr/bin/env python3
然后，通过命令给hello.py以执行权限：$ chmod a+x hello.py

Python对可变对象（字典或列表）传址，对不可变对象（数字、字符或元祖）传值。
is是身份运算符，判断两个对象的内存id是否相等
==是比较运算符，判断两个对象的值是否相等

Python 中的作用域（变量的作用域）
L （Local） 局部作用域
E （Enclosing） 闭包函数外的函数中
G （Global） 全局作用域
B （Built-in） 内建作用域
以 L –> E –> G –>B 的规则查找，即：在局部找不到，便会去局部外的局部找（例如闭包），再找不到就会去全局找，再者去内建中找。

三元运算写法
在赋值变量的时候，直接加判断，然后赋值格式
a=1;b=2
str0 = "choose1" if a > b else "choose2" ; print(str0)
print({True: "More", False: "Less"}[a > b]) #坑队友

lambda表达式
filter(lambda x: x % 2 == 1, range(1, 101))
def get_power(a, b):    return lambda x: a**b

*args, **kwargs 含义及用法。
args 是 arguments 的缩写，表示位置参数；
kwargs 是 keyword arguments 的缩写，表示关键字参数

字符串前缀
u"含有中文字符组成的字符串。"
r"\r\n”　　# 去掉反斜杠的转义机制。表示一个普通生字符串 \n\n，而不表示换行了。
b'<h1>Hello World!</h1>'     # b' ' 表示这是一个 bytes 对象。网络编程中，服务器和浏览器只认bytes 类型数据。
Python2中需要在文件头打上注释 # coding:utf-8 指定该程序使用的编码格式为UTF-8
编码 是将字符串转换成字节码，涉及到字符串的内部表示；'abcd'->(UTF-8)->\x61\x62\x63\x64
解码 是将字节码转换为字符串，将比特位显示成字符。
Unicode  str0='汉字'; str0=u'汉字';
type(str0)==<class 'str'> # python3中，字符串的存储方式都是以Unicode字符来存储的
UTF-8  str1=str0.encode('utf-8')
type(str1)==<class 'bytes'> #通过utf-8这种编码解码方式，将Unicode字符转换为对应的以字节方式存储的(3)个十六进制数。
GBK  str2=str0.encode('gbk')

\r是return 回车，使光标到行首。\n是next 换行，使光标下移一格。
Linux,Unix系统里，每行结尾只有“<换行>”，即"\n"；
Windows系统里面，每行结尾是“<回车><换行>”，即“\r\n”；
Mac系统里，每行结尾是“<回车>”，即"\r"；
---------------------------------------------------------------------
'''

'''
import this  #Python 之禅
The Zen of Python, by Tim Peters
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts. Special cases aren't special enough to break the rules.
Although practicality beats purity. Errors should never pass silently.
Unless explicitly silenced. In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch. Now is better than never.
Although never is often better than *right* now. If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''
'''
BaseException  # 所有异常的基类
 +-- SystemExit  # 解释器请求退出
 +-- KeyboardInterrupt  # 用户中断执行(通常是输入^C)
 +-- GeneratorExit  # 生成器(generator)发生异常来通知退出
 +-- Exception  # 常规异常的基类
      +-- StopIteration  # 迭代器没有更多的值
      +-- StopAsyncIteration  # 必须通过异步迭代器对象的__anext__()方法引发以停止迭代
      +-- ArithmeticError  # 各种算术错误引发的内置异常的基类
      |    +-- FloatingPointError  # 浮点计算错误
      |    +-- OverflowError  # 数值运算结果太大无法表示
      |    +-- ZeroDivisionError  # 除(或取模)零 (所有数据类型)
      +-- AssertionError  # 当assert语句失败时引发
      +-- AttributeError  # 属性引用或赋值失败
      +-- BufferError  # 无法执行与缓冲区相关的操作时引发
      +-- EOFError  # 当input()函数在没有读取任何数据的情况下达到文件结束条件(EOF)时引发
      +-- ImportError  # 导入模块/对象失败
      |    +-- ModuleNotFoundError  # 无法找到模块或在在sys.modules中找到None
      +-- LookupError  # 映射或序列上使用的键或索引无效时引发的异常的基类
      |    +-- IndexError  # 序列中没有此索引(index)
      |    +-- KeyError  # 映射中没有这个键
      +-- MemoryError  # 内存溢出错误(对于Python 解释器不是致命的)
      +-- NameError  # 未声明/初始化对象 (没有属性)
      |    +-- UnboundLocalError  # 访问未初始化的本地变量
      +-- OSError  # 操作系统错误，EnvironmentError，IOError，WindowsError，socket.error，select.error和mmap.error已合并到OSError中，构造函数可能返回子类
      |    +-- BlockingIOError  # 操作将阻塞对象(e.g. socket)设置为非阻塞操作
      |    +-- ChildProcessError  # 在子进程上的操作失败
      |    +-- ConnectionError  # 与连接相关的异常的基类
      |    |    +-- BrokenPipeError  # 另一端关闭时尝试写入管道或试图在已关闭写入的套接字上写入
      |    |    +-- ConnectionAbortedError  # 连接尝试被对等方中止
      |    |    +-- ConnectionRefusedError  # 连接尝试被对等方拒绝
      |    |    +-- ConnectionResetError    # 连接由对等方重置
      |    +-- FileExistsError  # 创建已存在的文件或目录
      |    +-- FileNotFoundError  # 请求不存在的文件或目录
      |    +-- InterruptedError  # 系统调用被输入信号中断
      |    +-- IsADirectoryError  # 在目录上请求文件操作(例如 os.remove())
      |    +-- NotADirectoryError  # 在不是目录的事物上请求目录操作(例如 os.listdir())
      |    +-- PermissionError  # 尝试在没有足够访问权限的情况下运行操作
      |    +-- ProcessLookupError  # 给定进程不存在
      |    +-- TimeoutError  # 系统函数在系统级别超时
      +-- ReferenceError  # weakref.proxy()函数创建的弱引用试图访问已经垃圾回收了的对象
      +-- RuntimeError  # 在检测到不属于任何其他类别的错误时触发
      |    +-- NotImplementedError  # 在用户定义的基类中，抽象方法要求派生类重写该方法或者正在开发的类指示仍然需要添加实际实现
      |    +-- RecursionError  # 解释器检测到超出最大递归深度
      +-- SyntaxError  # Python 语法错误
      |    +-- IndentationError  # 缩进错误
      |         +-- TabError  # Tab和空格混用
      +-- SystemError  # 解释器发现内部错误
      +-- TypeError  # 操作或函数应用于不适当类型的对象
      +-- ValueError  # 操作或函数接收到具有正确类型但值不合适的参数
      |    +-- UnicodeError  # 发生与Unicode相关的编码或解码错误
      |         +-- UnicodeDecodeError  # Unicode解码错误
      |         +-- UnicodeEncodeError  # Unicode编码错误
      |         +-- UnicodeTranslateError  # Unicode转码错误
      +-- Warning  # 警告的基类
           +-- DeprecationWarning  # 有关已弃用功能的警告的基类
           +-- PendingDeprecationWarning  # 有关不推荐使用功能的警告的基类
           +-- RuntimeWarning  # 有关可疑的运行时行为的警告的基类
           +-- SyntaxWarning  # 关于可疑语法警告的基类
           +-- UserWarning  # 用户代码生成警告的基类
           +-- FutureWarning  # 有关已弃用功能的警告的基类
           +-- ImportWarning  # 关于模块导入时可能出错的警告的基类
           +-- UnicodeWarning  # 与Unicode相关的警告的基类
           +-- BytesWarning  # 与bytes和bytearray相关的警告的基类
           +-- ResourceWarning  # 与资源使用相关的警告的基类。被默认警告过滤器忽略。
'''


def create_iterator(list_param):
    '''测试 __doc__ 输出，必须以"""*"""注释，引号嵌套时，区分单双
    #创建迭代器，    使用生成器推导式创建一个迭代器，并返回迭代器
    # 将列表推导式的“[]”改为“()”即为生成器推导式，众所周知，生成器返回一个迭代器对象'''
    return (value for value in list_param)


def main():
    # if __name__ == '__main__':
    # 遍历迭代器
    for i in create_iterator([1, 2, 3]):
        pass
        print(i)
    # 使用__doc__输出函数中的文档字符串属性
    print(create_iterator.__doc__)
    # 使用__dir__输出函数中的所有属性和方法
    print(create_iterator.__dir__())
# -----------------------------------------


def demo_func(*args, **kwargs):
    # arg是一个元祖类型
    print(args[1])
    # kwargs是一个字典类型
    print(kwargs.keys())


def main():
    # def if __name__ == '__main__':
    # 直接传参，但关键字类型必须为str
    demo_func(1, 2, 3, a=1, b=2)
    # 使用*和**进行解包
    demo_func(*(1, 2, 3), **{"a": 1, "b": 2})


demo_list = [str(i) * 10 for i in range(10)]
pp_object = pprint.PrettyPrinter(indent=4)  # indent是指句首缩进
# pp_object.pprint(demo_list)  # 整齐输出
# print(demo_list) #普通输出





