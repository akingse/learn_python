from numpy import *
from math import *
# n = 3.3
# for i in range(int(n)):
#     print(i)

from random import randint

# 1.创建一个包含20个学生名及成绩的字典创建方法
student_dict = {'student_%d' % i: randint(50, 100) 
								for i in range(1, 21)}

studentDict={}
for i in range(21):
    studentDict["student-"+str(i+1)]=randint(50, 100)
studentTuplelist=[]

k=studentDict.items() #items以列表返回可遍历的(键, 值) 元组数组
for iter in studentDict.items():
    studentTuplelist.append(iter)
# sortStudentTuplelist = sorted(studentTuplelist, reverse=False)

# 使用zip函数，将两个列表拼起来变成一个列表，因为返回的是一个对象所以使用list()函数转换一下
print(list(zip(studentDict.values(), studentDict.keys())))
# 然后对合成的元组列表进行排序
print(sorted(zip(studentDict.values(), studentDict.keys())))

# 方法2：
# 将字典的k:v以元组列表的形式返回
print(studentDict.items())
# 设置sorted的key参数为字典的value
print(sorted(studentDict.items(), key=lambda x: x[1]))




# 2.使用列表解析方法将学生字典转换为(value, key)的元组格式
student_tuplelist = [(stu_value, stu_key) for stu_key, stu_value
					in student_dict.items()]
# 查看以下转换后的效果
print(student_tuplelist)

# 3.使用sorted函数对元组列表student_list由分数高低进行排序
student_tuplelist_sorted = sorted(student_tuplelist, 
										reverse=True)

for iter in student_tuplelist_sorted:
    print(iter)
# print(student_tuplelist_sorted)



class MyNum(object):
    def __init__(self):
        self.__PI = 3.1415926

    @property
    def PI(self):
        return self.__PI


mynum = MyNum()
global m_pi
m_pi = mynum.PI
print(m_pi)


class CON:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


CON.PI = 3.14159
CON.PI = 4

CON.g_axis = 100


print(CON.PI)  # 3.14159
print(CON.g_axis)


# python复数
c = 1+1j
sq = sqrt(3)
# c=1+sq*j
c = complex(1, sq)/2

a = (-8)**(1/3)
print(c)
mat = array([[1, 2, 3],
             [4, 5, 7],
             [8, 9, 13]])


# print(linalg.inv(mat))
