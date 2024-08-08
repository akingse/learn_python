import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
mypath=r'C:\Users\Aking\source\repos\learn_python'
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
# create_geometry(trans(0,800,50)*scale(100,100,200)*Cone())
com=Combine(trans(-150,400,0)*scale(300)*Cube(),trans(300,400,0)*scale(100)*Cube())
com=Combine(trans(-150,400,0)*scale(300)*Cube())
# create_geometry(com)


# 在建筑环境测试
file=r'C:\Users\Aking\source\repos\bimbase\Bin\Release\OutputGraphicsToJson\\'
# js=JsonRead(file+'Graphics1.Json')
# js.write_python_code()

section=Section(Vec3(23450.00201413668,11299.999999999984,8950.0),
                Vec3(26399.99999999352+5,11299.999999999987,8950.0),
                Vec3(26400.000000006537-5,11099.999999999987,8950.0),
                Vec3(23450.002016770304,11099.999999999984,8950.0))
swept4=Swept(section, Vec3(0.0,0.0,500.0),) #main
# create_geometry(trans(-100,0)*swept4)

section=Section(Vec3(26300.000000000033,10900.326359186869,6300.0),Vec3(26300.000000000193,11299.999402089355,6300.0),Vec3(26600.000000000193,11299.999402089235,6300.0),Vec3(26600.000000000033,10900.326359186749,6300.0),Vec3(26300.000000000033,10900.326359186869,6300.0),)
swept15=Swept(section, Vec3(0.0,0.0,3150.0),)
# create_geometry(swept15)

section=Section(
    Vec3(49.99999999888371,54950.00000000931,17850),
    Vec3(49.99999999892316,54650.00000000931,17850),
    Vec3(49.999999998914745,54650.00000000931,18350),
    Vec3(49.99999999888678,54950.00000000931,18350),)
swept0=transz(-20)*rotate_arbitrary(Vec3(49.99999999888371,54950.00000000931,17850),Vec3(0,1,0),-0.005)*Swept(section, Vec3(14000.0,0.0,0.0),) 
create_geometry(swept0)



exit()
# 测试临界模糊布尔
cube=scale(200,200,1000)*Cube()
cube=trans(6,-1.5)*rotz(0.03)*scale(200,200,1000)*Cube()
create_geometry(cube)
create_geometry(trans(1000,0)*cube)
cube=trans(0,200,800)*scale(100,1000,200)*Cube()
create_geometry(trans(1000,0)*cube)
create_geometry(cube)

exit(0)

cube=trans(-2,0)*rotz(-0.03)*scale(200,150,200)*Cube()
create_geometry(cube)
# cube=trans(-0,0)*rotz(-0.0)*scale(200,150,200)*Cube()
create_geometry(trans(400)*cube)
cube=trans(0,100,-100)*scale(200,20,380)*Cube()
create_geometry(cube)
create_geometry(trans(400)*cube)
exit()

cone=Cone(Vec3(100,-50,0),Vec3(100,-50,500),20,20)
create_geometry(cone)
create_geometry(trans(-200)*cone)
cube=trans(100-10,-50,0.3)*scale(20,100,500)*Cube()
create_geometry(cube)
create_geometry(trans(-200)*trans(0,0,-0.)*cube)


exit()




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


