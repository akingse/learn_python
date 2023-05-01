

'''
@property

　　python中的@property装饰器可以总结为两个作用：

让函数可以像普通变量一样使用
对要读取的数据进行预处理
'''

class User():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def tag(self):
        return self.name + str(self.age)

user = User('xiao',5)
# print(user.tag())



class User():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @property
    def tag(self):
        return self.name + str(self.age)

user = User('xiao',5)
# print(user.tag) #没有括号，像变量一样



# 读取类属性前对数据进行预处理
class User():
    def __init__(self, name, age):
        self.name = name
        self._age = age

    @property
    def age(self):
        return self._age + 5 #装饰器处理

user = User('xiao',5)
print(user.age) #像变量一样，必须去掉括号