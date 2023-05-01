print() #防止第一段被注释
'''
Python二级  2019-9-23
基本要求
掌握Python语言的基本语法规则。
掌握不少于2个基本的Python标准库。
turtle jieba calender
掌握不少于2个Python第三方库，掌握获取并安装第三方库的方法。
能够阅读和分析Python程序。
熟练使用IDLE开发环境，能够将脚本程序转变为可执行程序。
了解Python计算生态的主要第三方库名称：网络爬虫、数据分析、数据可视化、机器学习、Web开发等
选择题40
程序题5*3+10+15+20
教材-《python程序设计（3）》John zelle 王海鹏
Python IDLE主窗口是一个 Python 语言的解释器，也被称为 Shell。
在IDLE中点击File-New File，会弹出一个.py对话框，此时可以编辑多行代码。
PyCharm是一种Python IDE，带有一整套可以帮助用户在使用Python语言开发时提高其效率的工具。
Anaconda指的是一个开源的Python发行版本，其包含了Python等180多个科学包及其依赖项。
Python发行版——从标准实现(CPython)到针对速度进行优化的版本(PyPy)，再到特殊用例(Anaconda、ActivePython)
乃至最初为完全不同的其他语言设计的运行时(Jython、IronPython)。
Anaconda Python的主要用例包括数学、统计学、工程、数据分析、机器学习以及其他相关应用。

Python373-Anaconda3-PyCharm201902
Alluser版，path编辑，添加第三方库
# a = 1 #autopep8测试
# 快捷键设置 file/settings/keymap
# main menu/run F5
# main menu/code ctrl+/
# python.exe -m pip install autopep8 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
# python.exe -m pip install autopep8 -i http://mirrors.aliyun.com/pypi/simple --trusted-host pypi.aliyun.com
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple
------------------------------------------------------------
学习网址
https://www.runoob.com/manual/pythontutorial3/docs/html/index.html#
https://www.runoob.com/python3/python3-tutorial.html

Python tips
高级数据结构使你可以在一条语句中表达复杂的操作；
语句组使用缩进代替开始和结束大括号来组织；
变量或参数无需声明。
Python3源码文件以 UTF-8 编码
语句很长，可以使用反斜杠(\)来实现多行语句，在 [], {}, 或 () 中的多行语句，不需要使用
空行也是程序代码的一部分。可以在同一行中使用多条语句，语句之间使用分号(;)分割
缩进相同的一组语句构成一个代码块，我们称之代码组。
print() 默认输出是换行的，不换行需要在变量末尾加上 end=""
将整个模块(somemodule)导入，格式为： import somemodule
导入某个函数,格式为： from somemodule import somefunction
模块中的全部函数导入，格式为： from somemodule import *

数学函数
abs() exp() ceil() floor() round() log(math.e) log10() max() min() pow() sqrt()
三角函数
atan2(y,x) hypot(x,y) degrees(math.pi) radians(rad)
随机数函数
choise(seq) 随机选择元素
random() 随机生成实数，范围[0,1)
seed([x]) 改变随机数生成器的种子seed
shuffle(list) 将序列的所有元素随机排序

迭代器
迭代器(Iterators)是一个可以记住遍历的位置的对象。
迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束。迭代器只能往前不会后退。
list0=[1,2,3,4]
it = iter(list0)    # 创建迭代器对象
print (next(it)) # next()每次只迭代一次
for x in it:    print (x, end=" ")

生成器
使用了 yield (让)的函数被称为生成器（generator）。
生成器是一个返回迭代器的函数，只能用于迭代操作。
每次遇到 yield 时函数会暂停并保存当前所有的运行信息，返回 yield 的值, 并在下一次执行 next() 方法时从当前位置继续运行。
--------------------------------------------------------------
标准数据类型6种
不可变数据：Number（数字）、String（字符串）、Tuple（元组）；
可变数据：List（列表）、Dictionary（字典）、Set（集合）。
序列类型：Sequence Types — list, tuple, str 

数字类型(Number)
数字有四种类型：整数、布尔型、浮点数和复数。int bool float complex
数字 N1,N2,N3,N4=1,1.0,True,1+1j,后缀 j 表示虚数部分。

字符串(String)
s='character_string'
转义符 '\'，使用r(raw string)原始字符串,可以让反斜杠不发生转义。repr()原符函数
Python中没有单独的字符类型；一个字符就是一个长度为1的字符串。
str[0:2] 字符串有两种索引方式，从左往右以 0 开始，从右往左以 -1 开始。
字符串可以被检索，切片，不可以被更改。截取的语法：变量[头下标:尾下标:步长]，前实后空。
字符串格式化 %s %d %f %e ,参考str.format()

列表 list=[,]
列表可以完成大多数集合类的数据结构实现。列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表。
列表中的元素是可以直接赋值改变。del list[0] 直接删除。二维列表索引 a[0][0]
列表当作堆栈使用，用 append() 方法可以把一个元素添加到堆栈顶。用不指定索引的 pop() 方法可以把一个元素从堆栈顶释放出来
列表当作队列使用，使用 collections.deque，它为在首尾两端快速插入和删除而设计。

元组 tuple=(,)
元组，与列表类似，不同之处在于元组的元素不能修改。
构造包含 0 或 1 个元素的元组的特殊语法规则。tup1 = ();tup2 = (1,)

集合 set={,}
集合中重复的元素被自动去掉，可以进行集合运算：差-，并|，交&,反交^
用{ } 或者 set() 函数创建集合，空集合必须用set()而不是{ }，因为{ }是用来创建一个空字典。

字典 dict={:}
字典是一种映射类型，字典用 { } 标识，它是一个无序的 键(key) : 值(value) 的集合。
构造函数 dict() 可以直接从键值对序列中构建字典。dict0=dict([('key0', 0), ('key1', 1)])
        列表   元组    集合   字典    数字   字符
name  | list   tuple   set   dict
r/w   |        read         
store | value  value   key   keys
order | seque  seque  chaos  chaos
initia|[1,'a'](1,'a'){1,'a'} {'a':1}
in    | append         add   d['k']=v
out   | li[0:]  tu[0]        d['a']

列表 
=> 集合 set()去重
=> 字典 dict() 嵌套转字典；dict(zip(list1,list2))两个列表转字典
=> 合并 a+b ；a.extend(b) ；a[0:0]=b
=> 合并成字符串 ''.join(list)

字典
=> 字符串 str()
=> 字典key和value互转 {value:key for key, value in a_dict.items()}
=> 分割 dict([(key, base[key]) for key in subkey])
=> 合并 dict(d1, **d2)

字符串
=> 列表 list()
=> 元组 tuple()
=> 集合 set()
=> 字典 eval("{'name':'aa', 'age':24}")
=> 切分字符 a.split(' ') #依据空格切分

切片
list=[]
list[a:b] # 从左到右，空为所有
list[a:b:step] #step步长，空为1，-1为倒序
'''

'''

模块
使用引用模块函数的表示法访问模块的全局变量，modname.itemname
包通常是使用用“圆点模块名”的结构化模块命名空间。A.B 的模块表示了名为 A 的包中名为 B 的子模块。

---------------------------------------
函数
函数是组织好的，可重复使用的，用来实现单一，或相关联功能的代码段。
函数 调用 会为函数局部变量生成一个新的符号表。
函数引用的实际参数在函数调用时引入局部符号表，因此，实参总是传值调用（这里的值总是一个对象 引用 ，而不是该对象的值）。
 一个函数被另一个函数调用时，一个新的局部符号表在调用过程中被创建。
没有 return 语句的函数确实会返回一个值，这个值被称为 None （这是一个内建名称）。
如果 None 值是唯一被书写的值，那么在写的时候通常会被解释器忽略（即不输出任何内容）。

深入 Python 函数定义
可以定义包含若干参数的函数,有默认参数值,关键字参数，可变参数列表，三种形式。
为一个或多个参数指定默认值。这会创建一个可以使用比定义时允许的参数更少的参数调用的函数
必需参数：和函数内部定义有关
关键字参数：函数调用使用关键字参数来确定传入的参数值。def name(a,b):
默认参数：如果没有传递参数，则会使用默认参数。 def name(a=0,b=1):
不定长参数：你可能需要一个函数能处理比当初声明时更多的参数。
星号 * 的参数会以元组的形式导入。def name([formal_args,] *var_args_tuple ): def name(arg1, *vartuple):
两个星号 ** 的参数会以字典的形式导入。 def name([formal_args,] **var_args_dict ): funname(1, a=2,b=3)

匿名函数
python 使用 lambda 来创建匿名函数。不使用 def 语句这样标准的形式定义一个函数。
仅仅能在lambda表达式中封装有限的逻辑进去，不能访问自己参数列表之外或全局命名空间里的参数。
name=lambda [arg1 [,arg2,.....argn]]:expression
return语句
return [表达式] 语句用于退出函数，选择性地向调用方返回一个表达式。不带参数值的return语句返回None。

变量作用域
程序的变量的访问权限决定于这个变量是在哪里赋值的。变量的作用域决定了在哪一部分程序可以访问哪个特定的变量名称。
L （Local） 局部作用域；E （Enclosing） 闭包函数外的函数中；G （Global） 全局作用域；B （Built-in） 内置作用域
全局变量和局部变量
定义在函数内部的变量拥有一个局部作用域，定义在函数外的拥有全局作用域。局部变量只能在函数内部访问，全局变量可以在整个程序范围内访问
Python 中只有模块（module），类（class）以及函数（def、lambda）才会引入新的作用域，
其它的代码块（如 if/else/、try/except、for/while等）是不会引入新的作用域的，也就是说这些语句内定义的变量，外部也可以访问
内部作用域修改外部作用域的变量时，global和nonlocal关键字。
------------------------------------------
数据结构
列表 extend() insert(,)-pop(); index()-count(); reverse()-sort();
list.append(x)	把一个元素添加到列表的结尾，相当于 a[len(a):] = [x]。
list.extend(L)	通过添加指定列表的所有元素来扩充列表，相当于 a[len(a):] = L。
list.insert(i, x)	在指定位置插入一个元素。例如 a.insert(0, x)会插入到整个列表之前，a.insert(len(a), x)相当于a.append(x)
list.remove(x)	删除列表中值为 x 的第一个元素。如果没有这样的元素，就会返回一个错误。
list.pop([i])	从列表的指定位置移除元素，并将其返回。如果没有指定索引，a.pop()返回最后一个元素。元素随即从列表中被移除。
list.clear()	移除列表中的所有项，等于del a[:]。
list.index(x)	返回列表中第一个值为 x 的元素的索引。如果没有匹配的元素就会返回一个错误。
list.count(x)	返回 x 在列表中出现的次数。
list.sort()	对列表中的元素进行排序。
list.reverse()	倒排列表中的元素。
list.copy()	返回列表的浅复制，等于a[:]。
堆栈：列表方法使得列表可以很方便的作为一个堆栈来使用，堆栈作为特定的数据结构，最先进入的元素最后一个被释放（后进先出）。
用 append() 方法可以把一个元素添加到堆栈顶。用不指定索引的 pop() 方法可以把一个元素从堆栈顶释放出来。
队列：列表当做队列用，只是在队列里第一加入的元素，第一个取出来；但是拿列表用作这样的目的效率不高。

元组序列
由若干逗号分隔的值组成，没有括号默认是元组类型。
元组在输出时总是有括号的，以便于正确表达嵌套结构。
集合
基本功能包括关系测试和消除重复元素。
支持推导式  a = {x for x in 'abracadabra' if x not in 'abc'}
字典
构造函数 dict() 直接从键值对元组列表中构建字典。dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
字典推导可以用来创建任意键和值的表达式词典。 {x: x**2 for x in (2, 4, 6)}
简单的字符串，使用关键字参数指定键值对有时候更方便。 dict(sape=4139, guido=4127, jack=4098)
-------------------------------------------------------------------
模块
模块是一个包含所有你定义的函数和变量的文件，其后缀名是.py。
模块可以被别的程序引入，以使用该模块中的函数等功能。这也是使用 python 标准库的方法。
执行 import 语句，如果模块在当前的搜索路径就会被导入。搜索路径由一系列目录名组成的，解释器依次从这些目录中去寻找所引入的模块。
搜索路径是在Python编译或安装的时候确定的，安装新的库应该也会修改。搜索路径被存储在sys模块中的path变量。print(sys.path) 
from 语句让你从模块中导入一个指定的部分到当前命名空间中。from modname import name; from modname import *
__name__属性来使该程序块仅在该模块自身运行时执行。 if __name__ == '__main__':
每个模块都有一个__name__属性，当其值是'__main__'时，表明该模块自身在运行，否则是被引入。 dir()获取模块内定义的所有名称
Python 本身带着一些标准的模块库，有些模块直接被构建在解析器里，能很高效的使用，甚至是系统级调用也没问题。
包
包是一种管理 Python 模块命名空间的形式，采用"点模块名称"。
目录只有包含一个叫做 __init__.py 的文件才会被认作是一个包。
import sound.effects.echo 必须使用全名去访问
from sound.effects import echo 此时不需要前缀
from sound.effects import *  找到这个包里面所有的子模块，都导入进来。定义文件 __init__.py 存在一个叫做 __all__ 的列表变量

------------------------------------------------------------------------
输入输出 .format()
print() 函数，使用 str.format() 函数来格式化输出值。
{0[0]}, {0[1]} # :前，数据的坐标
{:+.2f}  # :后，数据的格式 （+正负号，f保留小数点后两位）
{:0>2d} # 0待补符号；^<>对齐符号；2宽度；bdox，进制；
{:.,}  {:.%}  {:.e} #特殊格式  b o d x 进制
'''
import math
# print('{:0>2d}'.format(123))
# # print('{:.6f}'.format(math.pi))
print('{:.2e}'.format(1230))

'''
将输出的值转成字符串，可以使用 repr() 或 str() 函数来实现。
format() 函数，字符串格式化
读和写文件
open(filename, mode) 函数
   b  +  b+
r read
w write
a 追加
------------------------------------------------------------------------

错误和异常
1语法错误 Python 的语法错误或者称之为解析错。 缩进():
2异常处理 try语句
执行try子句，如果没有异常发生，忽略except子句，try子句执行后结束。
如果在执行try子句的过程中发生了异常，那么try子句余下的部分将被忽略。
except (RuntimeError, TypeError, NameError):
try except 语句还有一个可选的else子句。这个子句将在try子句没有发生任何异常的时候执行。
要抛出的异常由 raise 的唯一参数标识。它必需是一个异常实例或异常类（继承自 Exception 的类）。
3用户自定义异常
你可以通过创建一个新的异常类来拥有自己的异常。
4预定义的清理行为 with
一些对象定义了标准的清理行为，无论系统是否成功的使用了它，一旦不需要它了，那么这个标准的清理行为就会执行。
'''
'''例子程序
def test0():
    f = open("1.txt", "w")
    f.write("0000")
    f.close()
    
def test1():
    f = open("1.txt", "w")
    try:
        f.write("1111")
    except Exception:
        print("ERROR")
    finally:
        f.close()
        
def test2():
    with open("1.txt", "w") as f:
        f.write("2222")
        
'''
import functools
from functools import reduce
'''对于序列来讲，有三个函数式编程工具: filter()、map()和reduce()。
map(function,sequence)：把sequence中的值当参数逐个传给function，返回一个包含函数执行结果的 list
filter(function,sequence)：对sequence中的item依次执行function(item)，将执行结果为True的item组成一个List/String/Tuple(取决于sequence的类型)返回。
reduce(function,sequence)：function接收的参数个数只能为2，先把sequence中第一个值和第二个值当参数传给function，
    再把function的返回值和第三个值当参数传给function，然后只返回一个结果。
lambda 表达式是 Python 中创建匿名函数的一个特殊语法. (代码简洁;不增加额外变量)
     lambda 语法本身为 lambda 表达式，而它返回的函数我称之为 lambda 函数。或者称为匿名函数。
'''
def func(n): #阶乘 factorial
    return n<2 and 1 or n*func(n-1) # True and 1==1; False and 2==2;
# print(func(1))
# add = lambda x, y : x+y
# print(add(1,2))
list1 = [3,5,-4,-1,0,-2,-6]
# print(sorted(list1, key=lambda x: abs(x)))
list1.sort(key=lambda x: abs(x))
# print(list1)
# fact=lambda a,b:reduce(lambda x,y:x*y,range(a,b)) #reduce 连续操作函数
# print(fact(5,10))




