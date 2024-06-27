import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402

# 生成遮挡模型
sec1=scale(10)*Section(Arc())
sec2=rectangle_diagonal(Vec3(),Vec3(20,20))
fusion=sec2-sec1
# create_geometry(trans(-10,0)*fusion)


box1=trans(20,-20,20)*scale(20)*Cube()#遮挡成环
# create_geometry(box1)

box2=trans(150,-20,30)*scale(150,20,60)*Cube() #遮挡box
box3=trans(180,-50,50)*scale(150,100,20)*Cube() #互相遮挡
# create_geometry(box2)
# create_geometry(box2)
get_discrete_points_from_spline

mesh1=scale(100)*Cube()-trans(50,50)*scale(100)*Cube()
mesh2=trans(50,0)*scale(100)*Cube()-trans(0,50)*scale(100)*Cube()
# create_geometry(mesh1)
# create_geometry(mesh2)

# create_geometry(Line(Vec2(55,80),Vec2(93,127)))
# create_geometry(Line(Vec2(39,96),Vec2(141,163)))

# 共面问题
box1=rotz(pi/6)*scale(200)*Cube()
box2=rotz(pi/6)*trans(50,0,50)*scale(100)*Cube()
# create_geometry(trans(0,100)*box1)
# create_geometry(trans(0,100)*box2)

# 回头线
box1=scale(200,100,50*pi)*Cube()
box2=scale(100,100,50*pi)*Cube()
# create_geometry(trans(0,100)*box1)
# create_geometry(trans(50,0)*box2)

# 回头线测试模型
create_geometry(trans(0,800,50)*scale(100,100,200)*Cone())
com=Combine(trans(-150,400,0)*scale(300)*Cube(),trans(300,400,0)*scale(100)*Cube())
com=Combine(trans(-150,400,0)*scale(300)*Cube())
create_geometry(com)



exit()
# 填充轮廓计算，测试用例
createAll=false

# ----------------------------------------------------------------------
# 交叉布尔
# ----------------------------------------------------------------------
box0=scale(200,20,100)*Cube().colorGray()
box1=trans(50,-30)*rotz(pi/6)*box0
if (createAll):
    create_geometry(box0)
    create_geometry(box1-box0)


# ----------------------------------------------------------------------
# 交叉布尔
# ----------------------------------------------------------------------
box0=scale(200,20,100)*Cube().colorGray()
box1=trans(50,-30)*rotz(pi/6)*box0
if (createAll):
    create_geometry(transx(1000)*rotx(pi/6)*box0)
    create_geometry(transx(1000)*rotx(pi/6)*(box1-box0))

# ----------------------------------------------------------------------
# 完全遮挡
# ----------------------------------------------------------------------

box0=scale(200,20,100)*Cube().colorGray()
cone=Cone(Vec3(100,-50,20),Vec3(100,-50,80),20,20)
if (createAll):
    create_geometry(trans(0,1000,1000)*box0)
    create_geometry(trans(0,1000,1000)*cone)


# ----------------------------------------------------------------------
# 完全遮挡
# ----------------------------------------------------------------------

box0=scale(200,20,100)*Cube().colorGray()
cone=Cone(Vec3(100,50,20),Vec3(100,50,80),20,20)
if (createAll):
    create_geometry(trans(1000,1000,1000)*box0)
    create_geometry(trans(1000,1000,1000)*cone)


# ----------------------------------------------------------------------
# 带洞
# ----------------------------------------------------------------------

box=scale(200,20,100)*Cube()
win=trans(50,-10,40)*rotz(-pi/6)*scale(100,50,50)*Cube()
if (createAll):
    create_geometry(trans(0,2000,2000)*(box-win))


# ----------------------------------------------------------------------
# 
# ----------------------------------------------------------------------

box=scale(200,20,100)*Cube()
win=trans(50,-10,40)*rotz(-pi/6)*scale(100,50,50)*Cube()
if (createAll):
    create_geometry(trans(1000,2000,2000)*(box-win))
    create_geometry(trans(1000,2000,2000)*trans(50,-60,20)*scale(60)*Cube())


# ----------------------------------------------------------------------
# 
# ----------------------------------------------------------------------

box=scale(200,20,100)*Cube()
win=trans(50,-10,40)*rotz(-pi/6)*scale(100,50,50)*Cube()
if (createAll):
    create_geometry(trans(2000,2000,2000)*(box-win))
    create_geometry(trans(2000,2000,2000)*trans(50,-60,30)*scale(60)*Cube())


box=scale(200,20,100)*Cube()
win=trans(50,-10,40)*rotz(-pi/6)*scale(100,50,50)*Cube()
if (createAll):
    create_geometry(trans(3000,2000,2000)*(box-win))
    create_geometry(trans(3000,2000,2000)*trans(50,-60,60)*scale(60)*Cube())


