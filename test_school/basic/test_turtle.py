print()
'''turtle'''
import turtle #默认窗口 4*(375*325)
from turtle import *
import math
#海龟动作 移动和绘制
'''
forward() | fd() 前进
backward() | bk() | back() 后退
right() | rt() 右转
left() | lt() 左转
goto() | setpos() | setposition() 前往/定位
setx() 设置x坐标，直接设定，相对坐标原点
sety() 设置y坐标
setheading() | seth() 设置朝向
home() 返回原点
circle(radius, extent=None, steps=None) 画圆
.dot(size=None, *color) 画点
stamp() 印章
clearstamp() 清除印章
clearstamps() 清除多个印章
undo() 撤消
speed() 速度
position() | pos() 位置
towards() 目标方向
xcor() x坐标
ycor() y坐标
heading() 朝向
distance() 距离
设置与度量单位
degrees() 角度 #默认360度为一周
radians() 弧度
'''
# if __name__ == '__main__':
g3=math.sqrt(3)
def test():
    p=turtle
    p.speed(10) #数值大于 10 或小于 0.5 则速度设为 0，0最快，1-10逐渐变快
    p.forward(300) #fd()
    p.backward(150)
    p.left(180) #相对于forward，与backward无关
    p.forward(150)
    p.goto(150,50*g3)
    p.setheading(90) #单位默认为角度
    p.forward(100*g3)
    p.home()
    p.setx(150)
    p.sety(50*g3)
    print(p.position()) #输出元组xy坐标，元组
    print(p.heading()) #输出当前朝向
    p.setpos(300,0)
    print(p.pos())
    c=(150,0)
    p.setpos(c)
    p.circle(50*g3,360,10)
    p.dot(10,'cyan')
    p.color("blue")
    # a=p.stamp()
    # p.clearstamps(a)
    p.undo() #撤消最近的一个 (或多个) 海龟动作
    print(p.towards(0,0)) #朝向夹角
    print(p.xcor(),p.ycor())

    done()
# test()
# 获取海龟的状态
# 画笔控制
# 绘图状态
'''pendown() | pd() | down() 画笔落下
penup() | pu() | up() 画笔抬起
pensize() | width() 画笔粗细
pen() 画笔
isdown() 画笔是否落下
颜色控制
color() 颜色
pencolor() 画笔颜色
fillcolor() 填充颜色'''
# 填充
'''filling() 是否填充
begin_fill() 开始填充
end_fill() 结束填充
更多绘图控制
reset() 重置
clear() 清空
write() 书写'''
'''"shown": True/False
"pendown": True/False
"pencolor": 颜色字符串或颜色元组
"fillcolor": 颜色字符串或颜色元组
"pensize": 正数值
"speed": 0..10 范围内的数值
"resizemode": "auto" 或 "user" 或 "noresize"
"stretchfactor": (正数值, 正数值)
"outline": 正数值
"tilt": 数值'''
def test(): #x,y
    e=turtle
    # e.screensize(400, 300) #, 'white'
    # e.bgcolor("snow")
    # e.hideturtle()
    # e.showturtle()
    # e.shape("classic") # name=None "arrow", "turtle", "circle", "square", "triangle", "classic"
    e.speed(5)
    e.color("cyan")
    e.pendown()
    # print(e.isdown())
    e.pensize(2) #width=None e.width(3) #width=None False
    # e.pen(shown='False',pendown='False',fillcolor="red", pencolor="red",speed=5, pensize=3)
    # e.penup()
    e.pencolor('red')
    # print(e.pencolor())
    # e.circle(100, 360, 36)
    e.fillcolor('Tan')
    e.begin_fill()
    # e.goto(x,y) #承接onclick
    e.forward(300)
    e.pencolor('#0000FF') #纯蓝
    e.goto(150, 150 * g3)
    e.colormode(255) #提前设置颜色模式 0-255
    e.pencolor((0,128,128)) #tuple(r,g,b) 蓝色
    e.home()
    # e.fillcolor("violet")
    # print(e.filling())
    # e.color('snow')
    e.end_fill()
    print(sorted(e.pen().items()))
    # print(e.isdown()) #笔落下返回 True，如果画笔抬起返回 False。
    # e.clear()
    # e.reset() #从屏幕中删除海龟的绘图，海龟回到原点并设置所有变量为默认值。
    done()
# test()
# --------------------------------------
e=turtle
screen=turtle
# screen.screensize(500, 500,'white')
#原始尺寸 748*628 边框 +2*10 +2*10; 758*1.25=960;648*1.25+40=850
# e.resizemode()
# turtle.setworldcoordinates(-500,-500,500,500) #lowerleftx, lly, upperrightx, ury
screen.bgcolor("snow")
# screen.bgpic('D:\SogouExp\python-code\chapter04\TIM47.png') #picname=None

'''# e.tracer(1, 100)
for i in range(36): #以直代曲
    e.left(10)
    e.forward(20) #i*0.5
    e.delay(10) #毫秒，默认10
print(e.position())
e.hideturtle()'''

'''e.hideturtle()
e.tracer(8, 25)
dist = 0
for i in range(100):
    e.fd(dist)
    e.rt(90)
    dist += 4
print(e.position())'''

'''s = Shape("compound")#要使用由多个不同颜色多边形构成的复合海龟形状，你必须明确地使用辅助类 Shape，创建一个空 Shape 对象，类型为 "compound"。
poly1 = ((0,0),(100,-50),(0,100),(-100,-50))
s.addcomponent(poly1, "red", "cyan") # addcomponent() 方法向此对象添加多个部件。'填充颜色'，'轮廓颜色'
poly2 = ((0,0),(100,-50),(-100,-50))
s.addcomponent(poly2, "blue", "red")

turtle.register_shape("myshape", s) #将 Shape 对象添加到 Screen 对象的形状列表并使用它:
turtle.shape("myshape")
print(screen.screensize())'''

# e.forward(-150) #必须点击当前起始点
# turtle.ondrag(test) #(turtle.goto) #好多个，有毒
# turtle.onclick(test) # , btn=1, add=None
'''# class MyTurtle(Turtle):
#     def glow(self,x,y):
#         self.fillcolor("red")
#     def unglow(self,x,y):
#         self.fillcolor("")
# turtle = MyTurtle()
# turtle.onclick(turtle.glow)     # clicking on turtle turns fillcolor red,
# turtle.onrelease(turtle.unglow)'''
'''turtle.home()
turtle.begin_poly()
turtle.fd(100)
turtle.left(20)
turtle.fd(30)
turtle.left(60)
turtle.fd(50)
turtle.end_poly()
p = turtle.get_poly()'''
# p.register_shape("myFavouriteShape", p)
# turtle.clear()
# turtle.clearscreen()
# turtle.forward(100)
# turtle.reset() #针对移动
# turtle.resetscreen()


# 海龟状态
# 可见性
'''showturtle() | st() 显示海龟
hideturtle() | ht() 隐藏海龟
print(isvisible()) 是否可见'''
# 外观
'''shape() 形状
resizemode() 大小调整模式
shapesize() | turtlesize() 形状大小
shearfactor() 剪切因子
settiltangle() 设置倾角
tiltangle() 倾角
tilt() 倾斜
shapetransform() 变形
get_shapepoly() 获取形状多边形'''
# 使用事件
'''onclick() 当鼠标点击
onrelease() 当鼠标释放
ondrag() 当鼠标拖动'''
# 特殊海龟方法
'''begin_poly() 开始记录多边形
end_poly() 结束记录多边形
get_poly() 获取多边形
clone() 克隆
getturtle() | getpen() 获取海龟画笔
getscreen() 获取屏幕
setundobuffer() 设置撤消缓冲区
undobufferentries() 撤消缓冲区条目数
TurtleScreen/Screen 方法'''
# 窗口控制
'''bgcolor() 背景颜色
bgpic() 背景图片
clear() | clearscreen() 清屏
reset() | resetscreen() 重置
screensize() 屏幕大小
setworldcoordinates() 设置世界坐标系'''
# 动画控制
'''delay() 延迟
tracer() 追踪
update() 更新'''
# 使用屏幕事件
'''listen() 监听
onkey() | onkeyrelease() 当键盘按下并释放
onkeypress() 当键盘按下
onclick() | onscreenclick() 当点击屏幕
ontimer() 当达到定时
mainloop() | done() 主循环'''
turtle.title('titlename')
turtle.mode("world") # "standard", "logo" 或 "world" 其中之一
# turtle.setup(width=_CFG["width"], height=_CFG["height"], startx=_CFG["leftright"], starty=_CFG["topbottom"])
def fun():
    e.goto(0,0)
    e.lt(30)
    e.fd(150)
import winsound
def main():
    # turtle.setup(1280, 720, 0, 0) #设定窗口大小
    # turtle.ontimer(fun, t=0)
    # screen.onclick(fun)# fun(x,y);turtle.goto
    # screen.onclick(None)
    # fun()
    # screen.textinput("title", "Name of first player:")
    # screen.numinput("Poker", "Your stakes:", 1000, minval=0, maxval=10000)

    # screen.onkey(fun, 'Return')  # .onkey ;.onkeyrelease 释放生效，.onkeypress 按下生效
    screen.listen()
    print(turtle.getshapes()) #返回所有当前可用海龟形状的列表。
    print(turtle.turtles()) #返回屏幕上的海龟列表。
    # print(e.window_height(),e.window_width())
    # turtle.exitonclick() #点击关闭
    # turtle.bye() #win.close()

    '''for i in range(1,100):
        # winsound.Beep(int(600 * math.sin(i / 6.28) + 700), 150)
        winsound.Beep(i*37,150) #37 thru 32767
        # print(int(600 * math.sin(i / 6.28) + 700),end=' ')
        if i%10==0:
            print('\n')'''
    done()
# main()
# 设置与特殊方法
'''mode() 模式
colormode() 颜色模式
getcanvas() 获取画布
getshapes() 获取形状
register_shape() | addshape() 添加形状
turtles() 所有海龟
window_height() 窗口高度
window_width() 窗口宽度'''
# 输入方法
'''textinput() 文本输入
numinput() 数字输入
Screen 专有方法
bye() 退出
exitonclick() 当点击时退出
setup() 设置
title() 标题'''

'''p=Turtle()
p.color('red', 'yellow')
p.begin_fill()
while True:
    p.forward(200)
    p.left(170)
    if abs(p.pos()) < 1:
        break
p.end_fill()
done()'''

# -------------------------------------------------------------------
# drawtree.py  分形几何。一种基于递归的反馈系统
def tree(plist, l, a, f): #pen列表，初始枝干长度，分枝夹角，比例系数
    """ plist is list of pens
    l is length of branch #
    a is half of the angle between 2 branches
    f is factor by which branch is shortened from level to level. 缩短系数"""#tree([p], 110, 60, 0.618)
    n = 0
    if l > 8: #l=l*f=l*0.618**n #必须用if ，不满足 l>5，中止迭代
        pqlist = [] #每次迭代重置pqlist，相对上一层画分枝
        for p in plist: #把plist列表里的每个p对象，都执行一遍：直走l，分叉pq，加入新列表
            p.forward(l)#沿着当前的方向画画Move the turtle forward by the specified distance, in the direction the turtle is headed.
            q = p.clone()#Create and return a clone of the turtle with same position, heading and turtle properties.
            p.left(a) #Turn turtle left by angle units
            q.right(a)#Turn turtle right by angle units
            pqlist.append(p)#将元素增加到列表的最后
            pqlist.append(q)
            n += 1
        print(n,'-',l) #输出侧迭代结果，依次由内向外输出，如果放在tree(pqlist后面。好吧当我没说
        tree(pqlist, l*f, a, f) #调用自身，迭代法

def drawtree(x, y,theta):
    global p
    p = Turtle()
    p.color("green")
    p.pensize(3)
    p.hideturtle()
    p.getscreen().tracer(30, 10) #刷新速度
    p.penup();    p.goto(x, y);    p.pendown() #设定起始点
    # p.left(theta)
    p.setheading(theta)
    tree([p], 150, 60, 0.618)
    # print(len(p.getscreen().turtles())) #用了多少个turtle绘制
'''# drawtree(0, 0,90)
# p.penup();    p.goto(0,0);    p.pendown() #设定起始点
# p.setheading(-30)
# drawtree(-75*g3, 225,-30)
# done()'''
def main():
    drawtree(0, 0,-30)
    drawtree(0, 0, 90)
    drawtree(0, 0,-150)
    done()
# main()

# --------------------------------------------------------------------------------------
#关于颜色
def main():
    # turtle.color
    # turtle.pencolor
    # e.fillcolor = 'black' #箭头专属颜色
    # turtle.begin_fill()
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple']
    e=turtle
    # e.hideturtle()
    e.speed(0)
    for i in range(6):
        e.color(colors[i],colors[i+1])# 画笔 填充颜色
        e.begin_fill()# 开始填充
        e.right(60)# 第二个开始的角度（弧度）360度准备画几个
        e.circle(100) # 半径
        # e.end_fill()
    e.penup();
    e.goto(0,-100)
    e.pendown()
    e.pen(pencolor='red', pensize=1,fillcolor='cyan', outline=2) #
    # ('pendown', True), ('resizemode', 'noresize'), ('shearfactor', 0.0),
    # ('shown', True), ('speed', 10) ,('stretchfactor', (1.0, 1.0)), ('tilt', 0.0))#
    # e.write('0')
    e.circle(100)
    done()
# main()

#五角星图形
def main():
    p = Turtle()
    p.color('yellow')#"black",# 如果没有p.fillcolor("red") ，默认为.color()的颜色
    p.begin_fill()
    for i in range(5):
        p.forward(300)  #将箭头移到某一指定坐标
        p.right(144)    #当前方向上向右转动角度
    p.end_fill()
    done()
# main()
'''e.color('green','red')
e.begin_fill()#开始填充
for i in range(20):
	e.fd(300)#长度
	# rt(150)#角度 #i=10
	e.rt(162)#i=20
e.end_fill()#结束填充
done()#显示停留'''
# --------------------------------------------------------------
import random

class MyTurtle(turtle.Turtle):    # 画一个初始角度为x,边长为x的正方形
    def draw_square(self, x):
        self.setheading(x)
        for i in range(4):
            self.forward(x/2)
            self.left(360//4)
    # def get_color(self):# 随机获取rgb模式下的颜色的三个参数
    #     rgb = []
    #     # for i in range(3):
    #     #     rgb.append(random.randint(1, 255))
    #     return [30,144,255]#rgb
    def set_pen_color(self): # 设置画笔的颜色
        self.screen.colormode(255) #疑问
        # rgb = []
        # for i in range(3):
        #     rgb.append(random.randint(1, 255))
        # if i%2:
        #     self.pencolor('cyan')  #self.get_color()
        # else:
        self.pencolor('cyan')
def main(theta):
    t = MyTurtle()
    t.hideturtle()
    t.speed(0)
    t.getscreen().tracer(2, 10) #(2, 10)
    global i
    for i in range(360//theta*4+1): #while x:
        t.set_pen_color()
        t.draw_square(i*theta)
    # t.screen.mainloop()  # 效果图
    done()
# main(6)

