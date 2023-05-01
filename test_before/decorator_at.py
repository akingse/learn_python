# print("hello world")

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
# t(1)

# ---------------------------------
# https://www.runoob.com/w3cnote/python-func-decorators.html


# 一切皆对象
def hi(name="yasoob"):
    def greet():
        return "now you are in the greet() function"
    def welcome():
        return "now you are in the welcome() function"
    if name == "yasoob":
        return greet
    else:
        return welcome

ha = hi()#拷贝了一份函数
print(hi) # 函数所在内存地址
print(hi()) #如果你不放括号在它后面，那它可以被到处传递
print(hi()())#把一对小括号放在后面，这个函数就会执行

print(ha) # 对象名所在内存地址
print(ha()) #函数调用

print('--------------------------------------')
# ---------------------------------------------------------

def hi():
    return "hi yasoob!"
 
def doSomethingBeforeHi(func):
    print("I am doing some boring work before executing hi()")
    print(func())

# doSomethingBeforeHi(hi)

def a_new_decorator(a_func):
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction
 
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")
 
# a_function_requiring_decoration()
# a_new_decorator(a_function_requiring_decoration)()


@a_new_decorator #装饰器的作用就是为已经存在的对象添加额外的功能。
def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")
 
# a_function_requiring_decoration()

# ---------------------------------------------------------

from functools import wraps #外包装
 
def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")
    return wrapTheFunction
 
@a_new_decorator
def a_function_requiring_decoration():
    """Hey yo! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")

# a_function_requiring_decoration()
# print(a_function_requiring_decoration.__name__)

# 函数传参
import logging
def use_logging(func):
    logging.warning("%s is running" % func.__name__)
    func()

def foo():
    print('i am foo')

# use_logging(foo)

# 简单装饰器
def use_logging(func):
    def wrapper():
        logging.warning(" %s is running" % func.__name__)
        return func()   # 把 foo 当做参数传递进来时，执行func()就相当于执行foo()
    return wrapper

def foo():
    print('i am foo')

foo = use_logging(foo)  # 因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper
# foo()                   # 执行foo()就相当于执行 wrapper()

# @装饰器
def use_logging(func):
    def wrapper():
        logging.warning("%s is running" % func.__name__)
        return func()
    return wrapper

@use_logging #在函数开始定义的地方，这样就可以省略最后一步再次赋值的操作
def foo():
    print("i am foo")

foo()

def funA(a):
    print ('funA')

def funB(b):
    print ('funB')
    return b

@funA
@funB
def funC():
    print ('funC')

funC#()


# ------------------------------------------

# @property装饰器就是负责把一个方法变成属性调用的：

class Student(object):
 
    @property
    def score(self):
        return self._score
 
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
# 在对实例属性操作的时候，就知道该属性很可能不是直接暴露的，而是通过getter和setter方法来实现的。


