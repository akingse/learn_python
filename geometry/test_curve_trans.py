# 缓和曲线
import sys
import pygame

# 初始化pygame
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bezier Curve")

# 定义三个点
P0 = (100, 400)
P1 = (300, 50)
P2 = (500, 400)

# 定义进度和步长
t = 0
dt = 0.01

while 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 计算当前点的坐标
    x = int((1-t)**2 * P0[0] + 2*t*(1-t) * P1[0] + t**2 * P2[0])
    y = int((1-t)**2 * P0[1] + 2*t*(1-t) * P1[1] + t**2 * P2[1])

    # 绘制当前点
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)

    # 根据规则调整进度t和控制点P1
    if t >= 1:  # 到达终点
        t = 1
    elif t >= 0.5:  # 接近终点，从控制点移回起始点
        P1 = (P0[0] + P2[0] - P1[0], P0[1] + P2[1] - P1[1])
        t += dt
    else:  # 向控制点移动
        t += dt
        P1 = (P1[0] + dt*100, P1[1] + dt*50)

    # 刷新屏幕
    pygame.display.flip()
    # 控制帧率
    pygame.time.delay(10)

'''
缓和曲线指的是平面线型中，在直线与圆曲线、圆曲线与圆曲线之间设置的曲率连续变化的曲线。
缓和曲线是道路平面线性要素之一，它是设置在直线与圆曲线之间或半径相差较大的两个转向相同的圆曲线之间的一种曲率连续变化的曲线。
缓和曲线的作用：
1、缓和曲率——使曲率连续变化；
2、缓和超高——使横向坡度连续变化；
3、缓和加宽——使车道加宽连续变化。

缓和曲线的线型多种多样，如回旋线、三次抛物线、七次四项式型、半波正弦型、一波正弦型、双纽线、多心复曲线……

我国常用的线型有两种：三次抛物线、回旋线。其中三次抛物线是回旋线的近似结果。

定义：
回旋线是半径从无穷大一直变化到一定设计值的一段弧线。回旋线是曲率随着曲线长度成比例变化的曲线。公路、匝道常用的缓和曲线是回旋线，也叫放射螺旋线。
回旋线不仅线形美观，而且与驾驶员匀速转动方向盘由圆曲线驶入直线或者由直线驶入圆曲线的轨迹线相符合。

'''
# 直线到圆弧的回旋曲线，默认原点为曲率为零的起点，终点为曲率半径为R的缓圆点(第一象限)


def get_discrete_points_from_clothoid(R: float, A: float, disNum: int) -> list:
    pointList = []
    ls = A*A/R  # 回旋线总长度
    a = 1/(R*ls)  # 曲率变化率
    # k=a*l # 曲率
    for i in range(disNum):
        x = 0.0
        y = 0.0
        l = i/disNum*ls
        for n in range(20):
            x += (-1)**n*a**(2*n)*l**(4*n+1) / \
                math.factorial(2*n)/(4*n+1)/2**(2*n)
            y += (-1)**n*a**(2*n+1)*l**(4*n+3) / \
                math.factorial(2*n+1)/(4*n+3)/2**(2*n+1)
        pointList.append(GeVec2d(x, y))
    return pointList


points = get_discrete_points_from_clothoid(50, sqrt(100*pi/2*50), 100)
# show_points_line(points)

