
# 函数
# 函数是组织好的，可重复使用的，用来实现单一，或相关联功能的代码段。

# https://www.runoob.com/wp-content/uploads/2014/05/py-tup-10-26-1.png

# 在 python 中，类型属于对象，变量是没有类型的：
global a 
a=[1,2,3]

a="Runoob"
# [1,2,3] 是 List 类型，"Runoob" 是 String 类型，
# 变量 a 是没有类型，她仅仅是一个对象的引用（一个指针），可以是指向任意类型对象
print(type([1,2,3]))
print(type("Runoob"))
print(type(id(a))) 
print(id(a))# id() 函数来查看内存地址变化
# 不可变类型：变量赋值 a=5 后再赋值 a=10，这里实际是新生成一个 int 值对象 10，再让 a 指向它，而 5 被丢弃，不是改变 a 的值，相当于新生成了 a。
# 可变类型：变量赋值 la=[1,2,3,4] 后再赋值 la[2]=5 则是将 list la 的第三个元素值更改，本身la没有动，只是其内部的一部分值被修改了。

# python 函数的参数传递：

# 不可变类型：类似 C++ 的值传递，如整数、字符串、元组。如 fun(a)，传递的只是 a 的值，没有影响 a 对象本身。如果在 fun(a) 内部修改 a 的值，则是新生成一个 a 的对象。
# 可变类型：类似 C++ 的引用传递，如 列表，字典。如 fun(la)，则是将 la 真正的传过去，修改后 fun 外部的 la 也会受影响


def printinfo( **vardict ):
   "打印任何传入的参数"
   print ("输出: ")
#    print (arg1)
   print (vardict)
 
# 调用printinfo 函数
printinfo(a=2,b=3)

# 强制位置参数
# Python3.8 新增了一个函数形参语法 / 用来指明函数形参必须使用指定位置参数，不能使用关键字参数的形式。
# 在以下的例子中，形参 a 和 b 必须使用指定位置参数，c 或 d 可以是位置形参或关键字形参，而 e 和 f 要求为关键字形参:

def f(a, b, /, c, d, *, e, f):
    print(a, b, c, d, e, f)
f(10, 20, 30, d=40, e=50, f=60)



a = 10
def sum ( n ) :
    # a=11
    # global a
    n += a
    # a=11
    print ('a = ', a, ' , ','n = ', n )
  
sum(3)



a = 10
def test():
    b = a + 2 #仅仅访问全局变量 a
    print(b)
test()

a = 10
def test():
    a=1
    a = a + 1 #修改同名的全局变量，则认为是一个局部变量，必须先定义
    print(a)
test()


# ---------------------------------------------
# 对于函数来说，形式参数简称形参，是指在定义函数时，定义的一个变量名。
def foo(x, y, z):...
# 对于函数来说，实际参数简称实参。是指在调用函数时传入的实际的数据，这会被绑定到函数的形参上。
foo(5,2,0)

# 显式指定函数的参数类型及返回值类型
def function_demo(param_A: int, param_B: float, param_C: list, param_D: tuple) -> dict:
    pass
print("----------------------------------------")  

def log(pr):#将被装饰函数传入
    def wrapper():
        print("execute first")      
        return pr()#执行被装饰的函数
    return wrapper#将装饰完之后的函数返回（返回的是函数名）
@log
def pr():
    print("我是小小洋")

pr()
# -----------------------------------------------

def printme(str):
    "打印任何传入的字符串"
    print(str)
    return
# 调用 printme 函数，不加参数会报错
printme(1)

# 调用printme函数
printme(str="菜鸟教程")

name, age = 'a', 35


def printinfo(name, age=35):  # 函数参数不支持同时赋值
    "打印任何传入的字符串"
    print("名字: ", name)
    print("年龄: ", age)
    return


# 调用printinfo函数
printinfo(age=50, name="runoob")


print('_____________________________________________________')

# 函数传参顺序
# def a1(a1):
#     print(a1)
#     return a1
# def a2(a2):
#     print(a2)
#     return a2

# def a3(a3):
#     print(a3)
#     return a3

# def fun(a=a1(a),b=a2(b),c=a3(c)):
#     print(a1(a),a2(b),a3(c))
# fun(1,2,3)


print('_____________________________________________________')


def changeme(mylist):
    "修改传入的列表"
    for i in range(len(mylist)):
        mylist[i] = i+1
    mylist = [1, 2, 3, 4]  # 对可更改类型的引用进行修改
    print("函数内取值: ", mylist)
    return


def changeme1(mylist):
    "修改传入的列表"
    mylist.clear()
    for i in range(4):
        mylist.append(i+1)  # 修改的是传过来的对象的属性。
    print("函数内取值: ", mylist)
    return


# 调用changeme函数
mylist = [10, 20, 30]
changeme(mylist)
print("函数外取值: ", mylist)

