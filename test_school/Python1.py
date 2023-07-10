'''
#coding=utf-8  #UTF-8则包含全世界所有国家需要用到的字符，英文使用1字节，中文使用3字节来编码

#!/usr/bin/python #!/usr/bin/env python(推荐）
print ("hello world！派森"); #python 2.0；

def fib(n): #define Fibonacci function;
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a+b
    print()
fib(10)
'''
'''
----------------------------------------------------------------------------
python 标识符
标识符由字母、数字、下划线组成。标识符是区分大小写
Python中的保留字。这些保留字不能用作常数或变数，或任何其他标识符名称，关键字只包含小写字母；
and	exec	not	assert	finally	or	break	for	pass	class	from	print	continue	global	raise
def	if	return	del	import	try	elif	in	while	else	is	with	except	lambda	yield

行和缩进
Python 的代码块不使用大括号 {} 来控制类，函数以及其他逻辑判断。python 最具特色的就是用缩进来写模块；
缩进的空白数量是可变的，但是所有代码块语句必须包含相同的缩进空白数量，这个必须严格执行；
建议你在每个缩进层次使用 单个制表符Tab 或 两个空格 或 四个空格 , 切记不能混用；
可以使用斜杠（ \）将一行的语句分为多行显示；
可以使用引号( ' )、双引号( " )、三引号( 或 """ ) 来表示字符串；#''''''#段落注释
print() 默认输出是换行的，如果要实现不换行需要在变量末尾加上逗号 ；
代码组
复合语句，首行以关键字开始，以冒号( : )结束，该行之后的一行或多行代码构成代码组。
----------------------------------------------------------------------------
'''
'''
import pprint
import requests

re = requests.get("https://www.guokr.com/")
pprint.pprint(ret.content,decode())

class Guoke:
	def __init__(self):
	  pass

if __name__== '__main__'

'''

'''

# File: chaos.py
# A simple program illustrating chaotic behavior.
def main():
    print("This program illustrates a chaotic function")
    x = eval(input("Enter a number between 0 and 1: "))
    for i in range(10):
        x = 3.9 * x * (1 - x)
        print(x)
'''
'''
def main():
	print("test")
	x = eval(input("Enter a number: "))
	for i in range(10):  #只能限定次数吗
		i=i+1
		print(x+i)
main()
'''


from graphics import * #
from turtle import *


"""
def main():
    win = GraphWin("Click Me!")
    for i in range(100):
        p = win.getMouse()
        print("You clicked at:", p.getX(), p.getY())

main()


def main():
    win = GraphWin("Click and Type", 400, 400)
    for i in range(10):
        pt = win.getMouse()
        key = win.getKey()
        field = Text(pt, key)
        field.draw(win)
    
main()
"""
'''
def main():
    win = GraphWin("My Circle", 200, 200)
    c = Circle(Point(100,100), 100)
    c.draw(win)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done
'''
'''
win=GraphWin('shape')  #基本线条操作
p1=Point(50,60)
p1.getX()
p1.getY()

p1.draw(win)
p2=Point(140,100)
p2.draw(win)


center=Point(100,100)
circ=Circle(center,30)
circ.setFill('white')
circ.draw(win)
lable=Text(center,"this is a")
lable.draw(win)

rect=Rectangle(Point(30,30),Point(70,70))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
rect.draw(win)
oval=oval(Point(20,120),Point(180,200))
oval.draw(win)

win=GraphWin('shape') 
#lefteye=Oval(Point(0,0),Point(100,50))
lefteye=Circle(Point(50,50),10)
lefteye.setFill('yellow')
lefteye.setOutline('red')
righteye=lefteye.clone()
#righteye.move(20.0)

oval=Oval(Point(0,0),Point(200,100))
win=GraphWin()
oval.draw(win)
'''
'''
color('green','red')# 画笔颜色  填充颜色
begin_fill()#开始填充
for i in range(5):    
	fd(300)#长度    
	rt(144)#角度end_fill()#结束填充
	done()#显示停留



import turtle as t
t.pencolor('red')
for i in range(5):
    t.forward(100)
    t.right(144)
'''

fillcolor("red")
begin_fill()
while True:
    forward(200)
    right(144)
    if abs(pos()) < 1:  #查看画笔是否回到原点，回到原点时为真
        break           #回到原点，跳出循环
end_fill()

