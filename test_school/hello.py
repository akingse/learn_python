##
# '''
# #!/usr/bin/python3
# linux环境变量专用
# Windows环境变量
# # C:\Users\Akingse> where python
# # C:\ProgramData\Anaconda3\python.exe
# # C:\Users\Akingse\AppData\Local\Programs\Python\Python37\python.exe
# # C:\Users\Akingse\AppData\Local\Microsoft\WindowsApps\python.exe
# '''为什么注释里面还报错，转义符
# SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 136-137:

#!/ProgramData/Anaconda3/python.exe
# print("Hello, World!")
# print("Hello, pyhon!")
# data='F0E0D0C0B0A0'
# print(data[0:2])
# print(data[2:4])
from math import *
from signal import signal

import numpy
from numpy import *
a=[5]

def fun(a):
    a.append(10)

fun(a)
print(a)

sin(pi)

a=-1
# print(signal(a))
data = [[1,2],[3,4],[5,6]]
x = numpy.array(data)
print(x)



def math_cubic_real_root(num):
    if abs(num)<1e-10:
        return 0
    elif num>0:
        return num**(1/3)
    else:
        return -(-num)**(1/3)

# a=math.pow(-27,1/3)
a=math_cubic_real_root(-28)
print(a)

def math_sign(num):
    if num==0:
        return 0
    elif num>0:
        return 1
    else:
        return -1


def ternary_operator(a):
    return 1 if a==True else 0


print(ternary_operator(True))

info="thisishowishowmylove"
print(info.center(30,"-"))

