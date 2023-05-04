import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..//'))
from pyp3d import *

# color(1, 0, 0)
# color(0, 1, 0)
# color(0, 0, 1)

line=Line(GeVec3d(),GeVec3d(),GeVec3d())
a=len(line.parts)

is_line_on_same_plane
get_nested_parts_from_line


def xiangmingda_formula(arc: Arc):
    ax = get_scale_param(arc.transformation).x  # x方向长轴
    by = get_scale_param(arc.transformation).y  # y方向短轴
    a = max(ax, by)
    b = min(ax, by)
    e = sqrt(1-(b*b)/(a*a))
    t = 15  # iterate times, 级数项数
    sigma = 1.0
    iter = 1.0
    for i in range(1, t+1):
        iter = iter*((2*i-1)/(2*i))
        sigma = sigma-(iter*iter)*pow(e, 2*i)/(2*i-1)
    return 2*pi*a*sigma


def integral_x2(a=0, b=1):  # 积分函数
    dnum = 50
    xStart = a
    xEnd = b
    step = (xEnd-xStart)/dnum
    sigma = 0.0

    for i in range(dnum+1):
        x1 = xStart+step*i
        x2 = xStart+step*(i+1)
        s = (x2*x2+x1*x1)/2*step
        sigma = sigma+s
    return sigma
# --------------------------------------------------------------------


# 第二类椭圆积分
def get_discrete_points_from_ellipse(arc: Arc, n: int = 0, withEnd=False) -> list:
    # arc_second_integration
    if n == 0:
        n = 12  # arc.scope*180/pi
    ax = get_scale_param(arc.transformation).x  # x方向长轴
    by = get_scale_param(arc.transformation).y  # y方向短轴
    a = max(ax, by)  # long axis
    b = min(ax, by)  # short axis
    e = sqrt(1-(b*b)/(a*a))
    mat = get_orthogonal_matrix(arc.transformation)
    pStart = inverse_std(mat)*arc.pointStart  # to XoY
    pEnd = inverse_std(mat)*arc.pointEnd
    thStart = atan2(pStart.y, pStart.x)
    thEnd = atan2(pEnd.y, pEnd.x)
    disNum = 36000  # 设定步长，公式求积分
    if abs(thEnd) < PL_A:
        thEnd += 2*pi
    thetaList = [thStart]
    pointList = []
    mytimes = 0

    def _perimeter(th):  # # 椭圆周长积分公式
        # return sqrt((a*cos(th)) ** 2+(b*sin(th)) ** 2)
        return a*sqrt(1-e*e*sin(th)*sin(th))
    if abs(arc.scope-2*pi) < PL_A:  # switch perimeter formula
        intege = get_perimeter_of_arc(arc)
    else:
        intege = 0.0
        stepT = (thEnd-thStart)/disNum
        for i in range(disNum):
            intege = intege+(_perimeter(thStart+stepT*i) +
                             _perimeter(thStart+stepT*(i+1)))*stepT/2
        print('S=', intege)

# -------------------------------------------------------
    # 方法一

    # def arc_surface(x):  # 以直代曲，此方法误差过大
    #     return (b-a)*x*x/pi+a*x

    # x = 0
    # disList = linspace(0, pi/2, 20) #积分函数图像
    # for iter in disList:
    #     pointList.append(
    #         GeVec3d(iter*100, sqrt((a*cos(iter)) ** 2+(b*sin(iter)) ** 2)))

    # for i in range(n):
    #     x = quadratic_equation_of_one_variable(
    #         (b-a)/pi, a, -arc_surface(x)-sigma/n)[0]  # isometry = sigma/n  # 等距长度
    #     thetaList.append(x)

# -------------------------------------------------------------
    def math_bisection_method(a, b, xc, accu=PL_E6):  # 二分法求数值解
        # fun: FunctionType
        def function(x):
            return (_perimeter(xc)+_perimeter(x))*(x-xc)/2-(intege/n)
        c = (a + b) / 2.0
        while(abs(function(c)) > accu):
            c = (a + b) / 2.0
            if (function(a) * function(c) < 0):
                b = c
            elif (function(b) * function(c) < 0):
                a = c
            else:
                break
        return c

# 方法二
    # 实践证明，积分公式算的是theta射线与椭圆交点的弧长，需要转换
    # 此方法有精度问题，问题很大，处在n份积分离散上，梯形近似面积
    # for i in range(n):
    #     theta = math_bisection_method(0, pi/2, thetaList[-1])
    #     thetaList.append(theta)
    # AL = []  # 每段长度一致
    # for i in range(1, n):
    #     A = (_perimeter(thetaList[i]) +
    #          _perimeter(thetaList[i+1]))*(thetaList[i+1]-thetaList[i])/2
    #     AL.append(A)
    # per = 0  # 此积分法求周长
    # for i in range(n):
    #     iter = (_perimeter(thetaList[i])+_perimeter(
    #         thetaList[i+1]))*(thetaList[i+1]-thetaList[i])/2
    #     per += iter
    # print("per=", per)


# ---------------------------------------------------------------

#
# 方法三
    # 设定步长，误差较小，delta_theta
    #
    before = time.time()
    verti = 0.0
    stepA = pi/disNum  # fixed step
    theta = thStart
    lenList = []  # 验证，第二段确实偏大
    if withEnd:
        n = n-1
    for i in range(n-1):
        lenL = 0.0
        while(lenL-intege/n < 0):
            mytimes += 1
            # integral function a*sqrt(1-e*e*sin(th)*sin(th))
            # 调用函数多花费10%时间
            lenL += (_perimeter(theta) + _perimeter(theta+stepA)) * stepA/2
            # trape = (a*sqrt(1-e*e*sin(theta)*sin(theta)) +
            #          a*sqrt(1-e*e*sin(theta+stepA)*sin(theta+stepA))) * stepA/2
            theta += stepA
        thetaList.append(theta-stepA)
        lenList.append(lenL)
        verti += lenL
    after = time.time()
    print("time3=", after-before)
    print(mytimes)
    if withEnd:
        thetaList.append(thEnd)


# -----------------------------------------------
# 方法四
# 离散圆弧计算坐标,累加norm
# 想不三，由于大量三角函数计算，效率差一倍

    def _distance(point1, point2):
        return sqrt((point2[1]-point1[1])**2 + (point2[0]-point1[0])**2)

    before = time.time()
    dTh = pi/disNum
    pointList = [pStart]
    theta = thStart
    mytimes = 0

    if withEnd:
        n = n-1
    for i in range(n-1):
        lenP = 0.0
        while (lenP-intege/n < 0):
            mytimes += 1
            alpha1 = atan2(a/b*sin(theta), cos(theta))
            theta = theta+dTh
            alpha2 = atan2(a/b*sin(theta), cos(theta))
            lenP += _distance([a*cos(alpha1), b*sin(alpha1)],
                              [a*cos(alpha2), b*sin(alpha2)])
        point1 = GeVec3d(a*cos(alpha1), b*sin(alpha1))
        pointList.append(point1)
    if withEnd:
        pointList.append(pEnd)
    after = time.time()
    print("time4=", after-before)
    print(mytimes)

    show_points_line(pointList)
    # break
    # lenLast = 0.0
    # step = (thEnd-(theta-stepA))/disNum
    # for i in range(disNum):
    #     lenLast = lenLast+(_perimeter((theta-stepA)+step*i) +
    #                        _perimeter((theta-stepA)+step*(i+1)))*step/2
    # verti += lenLast
    # print("verti=", verti)

    # -----------------------------------------
    # universal
    # for iter in thetaList:
    #     # R = math_ellipse_perimeter(iter)  # OP
    #     # show_points_line([GeVec3d(100*iter, 0), GeVec3d(100*iter, 200)], 1)
    #     # show_points_line([GeVec3d(0, 0), GeVec3d(
    #     #     200*cos(iter), 200*sin(iter))], 1)
    #     # alpha = atan(a/b*tan(iter))  # convert angle theta to alpha
    #     # if(int(alpha/(pi/2)) != int(iter/(pi/2))):
    #     #     alpha += pi
    #     alpha = atan2(a/b*sin(iter), cos(iter))  # new method
    #     pointList.append(GeVec3d(a*cos(alpha), b*sin(alpha)))
    #     # create_geometry(trans(a*cos(iter), b*sin(iter))*scale(10)*Sphere())

    # # 每段长度验证(弧线)
    # dList = []
    # for i in range(n):
    #     per = 0  # 此积分法求周长
    #     stepT = 100
    #     for j in range(stepT):
    #         segmL = (thetaList[i+1]-thetaList[i])/stepT
    #         iter = (_perimeter(thetaList[i]+j*segmL)+_perimeter(
    #             thetaList[i]+(j+1)*segmL))*segmL/2
    #         per += iter
    #     dList.append(per)

    dSList = []  # 验证每段长度（直线）
    for i in range(n):
        d = norm(pointList[i+1]-pointList[i])
        dSList.append(d)
    # fuck，误差来源于直线和圆弧，这是圆弧长度的积分
    # lenA = sum(dList)
    lenSA = sum(dSList)

    return mat*pointList


# ---------------------------------------------------------------
# mian()
arc = scale(200, 100)*Arc(pi)

print("Rama", get_perimeter_of_arc(arc))
create_geometry(arc)
# arcP = get_perimeter_of_arc(arc)


# arcP1 = xiangmingda_formula(arc)
arcP2 = get_discrete_points_from_ellipse(arc, 11, True)
# show_points_line(arcP2)


def test_cos(a=100):
    pointList = []
    for iter in linspace(0, pi/2, 20):
        pointList.append(GeVec3d(iter*100, a*cos(iter)+100))
    return pointList


points = test_cos()
# show_points_line(points)

# print(integral_x2())
# print(exp(2))
# print(pow(e, 2))


arc = trans(50, 50)*scale(20)*Arc(pi/1)
sec1 = trans(0, 0, 100)*Section(arc, rotz(pi/2) * arc,
                                rotz(pi)*arc, rotz(-pi/2)*arc)
point1 = Vec3(100, 80)
point2 = Vec3(80, 100)
sec2 = Section(point1, point2, rotz(pi/2)*point1, rotz(pi/2)*point2,
               rotz(pi)*point1, rotz(pi)*point2, rotz(-pi/2)*point1, rotz(-pi/2)*point2)
# geo = loft_different(sec1, sec2)
# create_geometry(geo)

# -------------------------------------------------------
before = time.time()
for i in range(int(1e7)):
    a = math.pi*math.e  # 使用*比/节约时间1%
after = time.time()
print("time*", after-before)

before = time.time()
for i in range(int(1e7)):
    a = math.pi/math.e
after = time.time()
print("time/", after-before)
