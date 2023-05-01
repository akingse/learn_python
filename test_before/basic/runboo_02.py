print()
'''===========================================目录===============================================
#Pyhon程序设计 （第三版） John Zelle
1 计算机和程序
计算机：在可改变的程序控制下，存储和操作信息的机器。
软件主宰硬件，程序控制物理机器。程序员是计算机的控制者，而不是奴隶
算法：
计算机工作原理
编程语言 coding，精准无二义的机器语言
编译器，一个复杂的计算程序，接受一个高级语言源代码，并翻译成原始机器代码
------------------------------------------------------------------------------------------------------------------------
'''

'''
2 简单程序
软件开发过程，
输入、处理、输出 IPO模式
python标识符，表达式
c='12' #存储字符 '1','2'
print(c) #显示 12
字符串连接 c='wang'+'kingsheng'
print(<expr>,<expr>,end=' ') # (<>)表示语句片段填充，express表示一个表达式,end=' '可以使多句单行输出
input(<prompt>) #将键盘输入存储为字符串
eval(input()) #求值函数，将字符串类型转化为数值。安全问题
x,y = y,x #同时赋值，交换数值
for <var> in <sequence>:
for i in range(n): range()函数产生0->n-1的列表

3 数值计算
------------------------------------------------------------------------------------------------------------------------
4 对象和图形
------------------------------------------------------------------------------------------------------------------------
5 序列：字符串，列表，文件
# 数字-字符串-元组 列表-集合-字典

字符串操作
连接 +
重复 *
索引 str[]
切片 str[:]
长度 len()
遍历 for i in str
#编码 Unicode  ord('a') ; cha(97)
类型转换函数
float()
int()
str()
eval()
------------------------------------------------------------------------------------------------------------------------
6 函数
------------------------------------------------------------------------------------------------------------------------
7 if
------------------------------------------------------------------------------------------------------------------------
8 for while
------------------------------------------------------------------------------------------------------------------------
9 模拟与设计
------------------------------------------------------------------------------------------------------------------------
10 类
类-对象
class name: a=1;def fun(): #定义属性和方法(函数)
object=classname() #新建了一个类的对象，新建了类的实例，保存在变量objname中
object.fun() #从模块中引用命名是引用属性：表达式 modname.funcname 中，modname 是一个模块对象，funcname 是它的一个属性。
因此，模块的属性和模块中的全局命名有直接的映射关系：它们共享同一命名空间。

类对象支持两种操作：属性引用和实例化。
MyClass.i 和 MyClass.f 是有效的属性引用，分别返回一个整数和一个方法对象。
类的 实例化 使用函数符号 x = MyClass()。只要将类对象看作是一个返回新的类实例的无参数函数即可。
类倾向于将对象创建为有初始状态的。因此类会定义一个名为 __init__() 的特殊方法。参数通过 __init__() 传递到类的实例化操作上


------------------------------------------------------------------------------------------------------------------------
11 数据集合
------------------------------------------------------------------------------------------------------------------------
12 面向对象
类(Class): 用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。
方法：类中定义的函数。
类变量：类变量在整个实例化的对象中是公用的。类变量定义在类中且在函数体之外。类变量通常不作为实例变量使用。
数据成员：类变量或者实例变量用于处理类及其实例对象的相关的数据。
方法重写：如果从父类继承的方法不能满足子类的需求，可以对其进行改写，这个过程叫方法的覆盖（override），也称为方法的重写。
局部变量：定义在方法中的变量，只作用于当前实例的类。
实例变量：在类的声明中，属性是用变量来表示的。这种变量就称为实例变量，是在类声明的内部但是在类的其他成员方法之外声明的。
继承：即一个派生类（derived class）继承基类（base class）的字段和方法。继承也允许把一个派生类的对象作为一个基类对象对待。
例如，有这样一个设计：一个Dog类型的对象派生自Animal类，这是模拟"是一个（is-a）"关系（例图，Dog是一个Animal）。
实例化：创建一个类的实例，类的具体对象。
对象：通过类定义的数据结构实例。对象包括两个数据成员（类变量和实例变量）和方法。

类定义 class ClassName:    <statement-1>
类对象
类对象支持两种操作：属性引用和实例化。属性引用语法：obj.name。
类有一个名为 __init__() 的特殊方法（构造方法），该方法在类实例化时会自动调用
def __init__(self): #__init__() 方法可以有参数，参数通过 __init__() 传递到类的实例化操作上。
    self.data = []
x = MyClass()  #实例化类 MyClass，对应的 __init__() 方法就会被调用。
self代表类的实例，而非类。代表当前对象的地址，而 self.class 则指向类。
类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的第一个参数名称, 按照惯例它的名称是 self

继承
派生类的定义 class DerivedClassName(BaseClassName1):    <statement-1>
多继承 多继承的类定义形如下例:class DerivedClassName(Base1, Base2, Base3):    <statement-1>
方法重写
super() 函数是用于调用父类(超类)的一个方法。super(Child,c).myMethod() #用子类对象调用父类已被覆盖的方法

------------------------------------------------------------------------------------------------------------------------
13 算法设计与递归
# 递归
# 对于自身函数的引用
def fact(n): #斐波那契数列
    if n==0:
        return 1
    else:
        return n*fact(n-1)
# print(fact(10))
--------------------------------

'''
# Python3 标准库概览
# 操作系统接口
import os #os模块提供了不少与操作系统相关联的函数。
print(os.getcwd())  # 返回当前的工作目录

# 文件通配符
# glob模块提供了一个函数用于从目录通配符搜索中生成文件列表:
import glob
# print(glob.glob('*.py'))

# 命令行参数
# 通用工具脚本经常调用命令行参数。这些命令行参数以链表形式存储于 sys 模块的 argv 变量。
import sys
# print(sys.argv)
# 错误输出重定向和程序终止
# sys 还有 stdin，stdout 和 stderr 属性，即使在 stdout 被重定向时，后者也可以用于显示警告和错误信息。
# sys.stderr.write('Warning, log file not found starting a new one\n')
# 字符串正则匹配
# re模块为高级字符串处理提供了正则表达式工具。对于复杂的匹配和处理，正则表达式提供了简洁、优化的解决方案:
import re
s=re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
# print(s)

# 数学
# math模块为浮点运算提供了对底层C函数库的访问:
import math
# print(math.pi)
# random提供了生成随机数的工具。
import random
s=random.choice(['a','b','c'])
# print(s)
# 访问 互联网
# 有几个模块用于访问互联网以及处理网络通信协议。其中最简单的两个是用于处理从 urls 接收的数据的 urllib.request
from urllib.request import urlopen

from datetime import date
now = date.today()
print(now)
# 数据压缩
# 以下模块直接支持通用的数据打包和压缩格式：zlib，gzip，bz2，zipfile，以及 tarfile。
#  输出格式
# reprlib 模块为大型或深度嵌套的容器缩写显示提供了 :repr() 函数的一个定制版本:
import reprlib
reprlib.repr(set('supercalifragilisticexpialidocious'))
# 模板
# string 提供了一个灵活多变的模版类 Template ，使用它最终用户可以用简单的进行编辑。这使用户可以在不进行改变的情况下定制他们的应用程序。
# 格式使用 $ 为开头的 Python 合法标识（数字、字母和下划线）作为占位符。占位符外面的大括号使它可以和其它的字符不加空格混在一起。 $$ 创建一个单独的 $:

# 多线程
# 线程是一个分离无顺序依赖关系任务的技术。在某些任务运行于后台的时候应用程序会变得迟缓，线程可以提升其速度。一个有关的用途是在 I/O 的同时其它线程可以并行计算。
# 多线程应用程序的主要挑战是协调线程，诸如线程间共享数据或其它资源。为了达到那个目的，线程模块提供了许多同步化的原生支持，包括：锁，事件，条件变量和信号灯。
# 日志
# logging 模块提供了完整和灵活的日志系统。它最简单的用法是记录信息并发送到一个文件或 sys.stderr:

import logging
logging.debug('Debugging information')
# 列表工具
# 很多数据结构可能会用到内置列表类型。然而，有时可能需要不同性能代价的实现。
# array 模块提供了一个类似列表的 array() 对象，它仅仅是存储数据，更为紧凑。
from array import array
# 十进制浮点数算法
# decimal 模块提供了一个 Decimal 数据类型用于浮点数计算。相比内置的二进制浮点数实现 float，这个类型有助于 控制精度
from decimal import *
from decimal import Decimal
from fractions import Fraction
getcontext().prec = 50
# pm=Decimal(1) / Decimal(7)
pm=Decimal(1/10) #print(pm) #浮点数算法：争议和限制 ,出现在分母不是2的倍数时
print(1/10==0.1)
# print(round(float(1/10),20))
print(0.1+0.1==0.2) #历史原因吗
print(0.1+0.2==0.3) #(1+2==3)
print(1/10+2/10==3/10)
# 这是二进制浮点数的自然性质：它不是 Python 中的一个 bug，也不是你的代码中的 bug。你会看到所有支持硬件浮点数算法的语言都会有这个现象

# fractions 和 decimal 模块使得这些计算很简单:


p=Fraction.from_float(0.1)
# print(p)
# print(3602879701896397/36028797018963968)

# ----------------------------------------------
# 阿姆斯特朗数
def amustl(lower,upper):
    for num in range(lower, upper + 1):
        # 初始化 sum
        sum = 0
        # 指数
        n = len(str(num));#print(n)
        temp = num
        while temp > 0:
            digit = temp % 10
            sum += digit ** n
            temp //= 10
            #
        if num == sum:
            amu=num
            ar = []
            # 指数
            n = len(str(amu)); #3位数
            temp = amu
            while temp > 0:
                digit = temp % 10
                ar.append(digit )
                # sum += digit ** n
                temp //= 10
            print(amu,'=',end='')
            # for i in range(n):
            #     print(' +',ar[n-1-i],end='')
            # print(' =',end='')
            for i in range(n):
                print(' +',ar[n-1-i]**n,end='')
            print()
# amustl(100,1000)
# --------------------------------
# 二分法查找位置
def binarySearch(arr, l, r, x): #(数组，左，长度，右)
    # 基本判断
    if r >= l:
        mid = int(l + (r - l) / 2)
        # 元素整好的中间位置
        if arr[mid] == x:
            return mid
            # 元素小于中间位置的元素，只需要再比较左边的元素
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
            # 元素大于中间位置的元素，只需要再比较右边的元素
        else:
            return binarySearch(arr, mid + 1, r, x)

    else:
        # 不存在
        return -1
def main():
    # 测试数组
    arr = [2, 3, 4, 10, 40]
    x = 10
    result = binarySearch(arr, 0, len(arr) - 1, x)

    if result != -1:
        print("元素在数组中的索引为 %d" % result)
    else:
        print("元素不在数组中")

#插入排序
def insertionSort(arr):
    for i in range(1, len(arr)):

        key = arr[i]

        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
def main():
    arr = [12, 11, 13, 5, 6]
    insertionSort(arr)
    print("排序后的数组:")
    for i in range(len(arr)):
        print("{}".format(arr[i]),end=' ')
# 希尔排序
def shellSort(arr):
    n = len(arr)
    gap = int(n / 2)
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap = int(gap / 2)
def main():
    arr = [12, 34, 54, 2, 3]
    shellSort(arr)
    print("\n排序后:")
    # for i in range(len(arr)):
    #     print(arr[i]),
