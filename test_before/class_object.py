class Person(object):
    __slots__ = ('name', 'age', 'sex')

    def __init__(self, name, age):
        self.name = name
        self.age = age


p = Person('lucy', 18)
print(p.__class__)  # <class '__main__.Person'>

s = ('a', 'b', 'c')
print(max(s))  # 排序时后面的字符更大


class Peopre(object):
    pass


# 内置属性
print(dir(Peopre))

'''
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
 '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', 
 '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', 
 '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
  '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
'''


def funcA(): pass


print(funcA.__name__)
print(funcA.__class__)
print(funcA.__doc__)
print(funcA.__module__)
print(funcA.__sizeof__)
print(funcA.__getattribute__)

print('-----------------------------------------------------')
print(dir(str))  # 查看str能够执行的操作. 内部的方法
# __iter__  字符串可以被迭代. 发现了__iter__
print(dir(list))
print(dir(open("x", mode="w")))  # int中没有__iter__

#  简单的下一个结论. 主要这个数据类型可以执行__iter__ 可以被迭代的数据类型
lst = ["汉高祖", "唐高祖", "明高祖", "哈哈", "娃哈哈", "爽歪歪"]
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

def add(a, b):
    '''
    "这是 add 函数文档"
    说明文档必须放前面
    '''
    return a+b

# print(add.__doc__)

class Person(object):
    def __init__(self,name='name',score=100):
        self.name = name
        self.score = score
        
# student = Person('Gavin',100)    #  传入 __init__ 方法中需要的 参数
student = Person( )
# print(student.name)
# print(student.score)



class Person(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def add(self):
        sum = self.x + self.y
        return sum
    
    def square(self):
        squr = pow(self.x,2)+pow(self.y,2)
        return squr
    def add_square(self):
        c = self.add()+self.square()
        return c
        
student = Person(3,4)
print(student.add())
print(student.square())
print('--------- 我是可爱的分割线-----------')
