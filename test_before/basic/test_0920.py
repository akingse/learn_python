import turtle, time
import winsound
import math
from turtle import *

def drawGap():
    turtle.penup()
    turtle.fd(5)

def drawLine(draw):
    drawGap()
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    drawGap()
    turtle.right(90)

def drawDigit(d):
    drawLine(True) if d in [2, 3, 4, 5, 6, 8, 9] else drawLine(False)  # g
    drawLine(True) if d in [0, 1, 3, 4, 5, 6, 7, 8, 9] else drawLine(False)  # c
    drawLine(True) if d in [0, 2, 3, 5, 6, 8, 9] else drawLine(False)  # d
    drawLine(True) if d in [0, 2, 6, 8] else drawLine(False)  # e
    turtle.left(90)  # 经历一次右转后，调整左转，方向竖直向上
    drawLine(True) if d in [0, 4, 5, 6, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 2, 3, 5, 6, 7, 8, 9] else drawLine(False)
    drawLine(True) if d in [0, 1, 2, 3, 4, 7, 8, 9] else drawLine(False)
    turtle.left(180)
    turtle.penup()
    turtle.fd(20)

def drawDate(date):
    turtle.pencolor('red')
    if '+' in date:
        for i in date:
            if i == '-':
                turtle.write('时', font=('Arial', 18, 'normal'))
                turtle.pencolor('green')
                turtle.fd(40)
            elif i == '=':
                turtle.write('分', font=('Arial', 18, 'normal'))
                turtle.pencolor('blue')
                turtle.fd(40)
            elif i == '+':
                turtle.write('秒', font=('Arial', 18, 'normal'))
                turtle.pencolor('yellow')
                turtle.fd(40)
            else:
                drawDigit(eval(i))
    else:
        turtle.goto(-180,-50)
        turtle.write(date, font=('Arial', 70, 'normal'))   # 打印超时文字

def init():
    turtle.setup(1280, 720, 0, 0)  # 设置画布大小 200 200 为屏幕位置
    turtle.speed(10)
    turtle.penup()
    turtle.goto(0, 0)
    turtle.fd(-200)     # 画笔起始位置
    turtle.pensize(5)

def main(book_time):
    over_flag = False
    beep_flag = True
    # count = book_time - time.time() + 0    # 画面延时n秒自动关闭
    try:
        while True:
            over_time = book_time - time.time()
            # count -= 1
            if over_time > 0:
                time_string = time.strftime("%M=%S+", time.localtime(over_time))
            else:
                time_string = 'Time out !!'
                over_flag = True
            turtle.clear()
            init()
            turtle.getscreen().tracer(30, 0)
            drawDate(time_string)  # 格式化时间 2017-05=02+ 控制输入年日月
            time.sleep(1)
            turtle.hideturtle()
            if over_flag and beep_flag:
                for i in range(100):
                    winsound.Beep(int(600 * math.sin(i / 6.28) + 700), 100)
                beep_flag = False
    except:
        pass

minites = 60 * 0.1
book_time = time.time() + minites
# main(book_time)
# done()
# -----------------------------------------------------------------------
from turtle import *
from time import sleep
e=turtle
def go_to(x, y):
   e.up()
   e.goto(x, y)
   e.down()
# go_to(100, 100)

def big_Circle(size):  #函数用于绘制心的大圆
   e.speed(0)
   for i in range(150):
       e.forward(size)
       e.right(0.3)
# big_Circle(1)
def small_Circle(size):  #函数用于绘制心的小圆
   for i in range(210):
       e.forward(size)
       e.right(0.786)

def heart( x, y, size):
   go_to(x, y)
   e.left(150)
   e.begin_fill()
   e.forward(50*size)
   big_Circle(size)
   small_Circle(size)
   e.left(120)
   small_Circle(size)
   big_Circle(size)
   e.forward(50*size)
   e.end_fill()

def arrow():
   e.pensize(10)
   e.pencolor('red')
   e.setheading(0)
   go_to(-400, 0)
   e.left(15);   e.forward(900)

def arrowHead():
   e.pensize(1)
   # e.speed(10)
   e.color('red')
   e.begin_fill()
   e.left(120);   e.forward(20)
   e.right(150);   e.forward(35)
   e.right(120);   e.forward(35)
   e.right(150);   e.forward(20)
   e.end_fill()


def main():
    turtle.setup(1280, 720, 0, 0)
    e.pensize(2)
    e.getscreen().tracer(1, 0) #取消注释后，快速显示图案
    arrow()  # 画出穿过两颗心的直线
    arrowHead()  # 画出箭的箭头

    e.color('red', 'pink')  # 轮廓，填充
    e.setheading(0)  # 使画笔的方向朝向x轴正方向
    heart(200, 0, 1)          #画出第一颗心，前面两个参数控制心的位置，函数最后一个参数可控制心的大小
    e.setheading(0)             #使画笔的方向朝向x轴正方向
    heart(-60, -80, 1.2)     #画出第二颗大心
    go_to(400, -300)
    e.write("520Python", move=True, align="left", font=("宋体", 30, "normal"))
    done()

main()
done()