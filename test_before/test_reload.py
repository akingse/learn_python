

'''
算术运算符的重载:
    方法名                  运算符和表达式      说明
    __add__(self,rhs)        self + rhs        加法
    __sub__(self,rhs)        self - rhs         减法
    __mul__(self,rhs)        self * rhs         乘法
    __truediv__(self,rhs)   self / rhs          除法
    __floordiv__(self,rhs)  self //rhs          地板除
    __mod__(self,rhs)       self % rhs       取模(求余)
    __pow__(self,rhs)       self **rhs         幂运算

'''
class Mylist:
    def __init__(self, iterable=()):
        self.data = list(iterable)
 
    def __repr__(self):
        return 'Mylist(%s)' % self.data
 
    def __add__(self, lst):
        return Mylist(self.data + lst.data)
 
    def __mul__(self, rhs): #默认对符号右侧变量作用
        # rhs为int类型,不能用rhs.data
        return Mylist(self.data * rhs)

    def __rmul__(self, rhs): #反向算术运算符的重载
        return Mylist(self.data * rhs)


 
L1 = Mylist([1, 2, 3])
L2 = Mylist([4, 5, 6])
L3 = L1 + L2
print(L3)  # Mylist([1,2,3,4,5,6])
L4 = L2 + L1
print(L4)  # Mylist([4,5,6,1,2,3])
# L5 = L1 * 3
# print(L5)  # Mylist([1,2,3,1,2,3,1,2,3])


list1=[1,1,2,2]
# print(list1*2)
# print(2*list1)

L5 = 3*L1
# print(L5)

class Mylist:
    def __init__(self, iterable=()):
        self.data = list(iterable)
 
    def __repr__(self):
        return 'Mylist(%s)' % self.data
 
    def __add__(self, lst):
        print('__add__被调用')
        return Mylist(self.data + lst.data)
 
    def __mul__(self, rhs):
        # rhs为int类型,不能用rhs.data
        print('__mul__被调用')
        return Mylist(self.data * rhs)
 
    def __rmul__(self, lhs):
        print("__rmul__被调用")
        return Mylist(self.data * lhs)
 
 
L1 = Mylist([1, 2, 3])
L2 = Mylist([4, 5, 6])
L3 = 3 * L1
# print(L3)
L1 += L2
# print(L1)
L2 *= 3
# print(L2)

'''
    位运算符重载

            方法名              运算符和表达式        说明
        __and__(self,rhs)       self & rhs            位与
        __or__(self,rhs)        self | rhs            位或
        __xor__(self,rhs)       self ^ rhs            位异或
        __lshift__(self,rhs)    self <<rhs            左移
        __rshift__(self,rhs)    self >>rhs            右移

    反向位运算符重载

              方法名            运算符和表达式         说明
        __and__(self,lhs)       lhs & rhs              位与
        __or__(self,lhs)        lhs | rhs              位或
        __xor__(self,lhs)       lhs ^ rhs              位异或
        __lshift__(self,lhs)    lhs <<rhs              左移
        __rshift__(self,lhs)    lhs >>rhs              右移

    复合赋值位相关运算符重载
    都是r，打错了
            方法名              运算符和表达式        说明
        __iand__(self,rhs)       self & rhs          位与
        __ior__(self,rhs)        self | rhs              位或
        __ixor__(self,rhs)       self ^ rhs            位异或
        __ilshift__(self,rhs)    self <<rhs           左移
        __irshift__(self,rhs)    self >>rhs           右移


    一元运算符的重载

     方法名              运算符和表达式        说明
     __neg__(self)         - self           负号
     __pos__(self)         + self           正号
     __invert__(self)      ~ self           取反
'''

# xor
# __xor__(self,rhs)       self ^ rhs            位异或
# __ixor__(self,rhs)      self ^ rhs            位异或

class MyXOR(): #重载
    def __init__(self, data):
        self.data = data
    def __xor__(self,rhs):
        return self.data**rhs

    def __rxor__(self,lhs):
        return self.data**4

print('-----------------------')
num=MyXOR(2)
print(num^3) # __xor__(self,rhs):
print(1^num) #__rxor__(self,lhs):

class Mylist:
    def __init__(self, iterable=()):
        self.data = list(iterable)
 
    def __repr__(self):
        return 'Mylist(%s)' % self.data
 
    def __neg__(self):
        g = (-x for x in self.data) #符号取反
        return Mylist(g)
 
    def __pos__(self):
        g = (abs(x) for x in self.data) #abs强转正号
        return Mylist(g)
 
 
l1 = Mylist([1, -2, 3, -4, 5, -6])
# l2 = - l1
# print(l2)
# l3 = +l1
# print(l3)


'''
特性属性@property
    实现其他语言所拥有的getter和setter功能

    作用:
        用来模拟一个属性
        通过@property装饰器,可以对模拟属性的赋值和取值加以控制

'''

class Student:
    def __init__(self, s):
        self.__score = s
 
    @property
    def score(self):
        # print('getter被调用')
        if 0 <= self.__score <= 1: #初始化预处理----------------------------------
            self.__score = 2
            # raise ValueError("paramter error!")

        return self.__score
 
    @score.setter # 装饰器预处理-----------------------------------------
    def score(self, s):
        '''此方法用设置值加以限制以保证数据的准确性setter是用来数据的'''
        if 0 <= s <= 1:
            self.__score = -1
 
    # def getScore(self, s):
    #     '''getter只是用来获取数据'''
    #     return self.__score
 
 

s = Student(0)
print('成绩是：', s.score)
s.score=0
print('成绩是：', s.score)
# s.setScore(100)
# s1 = s.score

class Indexer:
    def __init__(self,a,b):
        self.first=a
        self.second=b
    def __getitem__(self,index):
        if index==0:
            return self.first
        elif index==1:
            return self.second
        else:
            raise ValueError("something wrong!")


tt=Indexer(1,2)
print(tt[0])
print(tt[1])

