import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402

# 填充轮廓计算，测试用例
createAll=false

# ----------------------------------------------------------------------
# 交叉布尔
# ----------------------------------------------------------------------
box0=scale(200,20,100)*Cube().colorGray()
box1=trans(50,-30)*rotz(pi/6)*box0
if (not createAll):
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


