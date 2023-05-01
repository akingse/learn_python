
a = 1
int(a)
print(type(a))

b = a/2
c = a//2  # 整除
d = a*2
d = a**2 #幂


print(b, c)

def example(a, b):
    # return a,b
    return (a, b)


print(type(example(3, 4)))


def test(*args):
    print(args)
    return args


print(type(test(1, 2, 3, 4)))


# ---------------------------------

def timeit(func):
    def run(*argv):
        print(func.__name__)
        if argv:
            ret = func(*argv)
        else:
            ret = func()
        return ret
    return run


@timeit
def t(a):
    print(a)


t(1)


print('-----------------------------------------------------')
print(dir(str))  # 查看str能够执行的操作. 内部的方法
# __iter__  字符串可以被迭代. 发现了__iter__
print(dir(list))
print(dir(open("x", mode="w")))  # int中没有__iter__

#  简单的下一个结论. 主要这个数据类型可以执行__iter__ 可以被迭代的数据类型
lst = ["汉高祖", "清高祖", "明高祖", "哈哈", "娃哈哈", "爽歪歪"]
it = lst.__iter__()  # <list_iterator object at 0x000001ED54B17128> iterator 迭代器
print(it)
print(dir(it))  # 迭代器本身是可迭代的
# 可以使用__next__获取数据
print(it.__next__())  # 汉高祖
print(it.__next__())  # 清高祖
print(it.__next__())  # 明高祖
print(it.__next__())  # 明高祖
print(it.__next__())  # 明高祖
print(it.__next__())
print('-----------------------------------------------------')


a = 3  # strings, tuples, 和 numbers 是不可更改的对象
# 不可变类型：变量赋值 a=5 后再赋值 a=10，这里实际是新生成一个 int 值对象 10，再让 a 指向它，而 5 被丢弃，不是改变a的值，相当于新生成了a。


def change(a):
    a += 1
    return


change(a)
# 传递的只是a的值，没有影响a对象本身。比如在 fun（a）内部修改 a 的值，只是修改另一个复制的对象，不会影响 a 本身。
print(a)

print('_____________________________________________________')


def change(a):
    #  id() 函数来查看内存地址变化
    print(id(a))   # 指向的是同一个对象
    a = 10
    print(id(a))   # 一个新对象
# 调用函数前后，形参和实参指向的是同一个对象（对象 id 相同），在函数内部修改形参后，形参指向的是不同的 id。


a = 1
print(id(a))
change(a)


def printme(str):
    "打印任何传入的字符串"
    print(str)
    return


# 调用 printme 函数，不加参数会报错
printme(1)


def printme(str):
    "打印任何传入的字符串"
    print(str)
    return


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


def add(a, b):
    '''
    "这是 add 函数文档"
    说明文档必须放前面
    '''
    return a+b


print(add.__doc__)
