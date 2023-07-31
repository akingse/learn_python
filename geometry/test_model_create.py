import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402



# exit()
# 射线法测试-凹多面体
# create_geometry(trans(0,0,-1)*Extrusion([Vec3(-2, -1), Vec3(1, -1), Vec3(1, 0), Vec3(2, 0),
#                 Vec3(2, -1), Vec3(3, -1), Vec3(3, 2), Vec3(-2, 2)], Vec3(0, 0, 2)))
# create_geometry(scale(0.5)*Cube())
# create_geometry(translate(0,-0.5,0)*scale(0.5)*Cube())
# create_geometry(translate(2,-1,-1)*scale(1)*Cube())
exit()

# 点在线上，误差的影响
point=rotz(pi/3)*Vec3(1.1, 1.2,-1)
trigon=rotz(pi/3)*[Vec3(0,0),Vec3(2.2,2.4)]
cp=(point - trigon[1]).cross(point - trigon[0])

# cube1=transx(100)*Extrusion([Vec3(0,0),Vec3(100,0),Vec3(100,100),Vec3(0,100)],Vec3(0,0,100))
# cube2=trans(50,0,50)*rotz(pi/4)*Extrusion([Vec3(0,0),Vec3(100,0),Vec3(100,100),Vec3(0,100)],Vec3(0,0,100))
cube2=trans(50,0,50)*rotz(pi/2)*Extrusion([Vec3(0,0),Vec3(100,0),
                                           Vec3(30,0),Vec3(30,50),Vec3(70,50),Vec3(70,0),Vec3(100,0),
                                           Vec3(100,100),Vec3(0,100)],Vec3(0,0,100))
cube1=trans(70,50)*scale(0.5,0.5)*Extrusion([Vec3(100,0),Vec3(0,100),Vec3(-100,0),Vec3(0,-100)],Vec3(0,0,100))
cube2=trans(50,0,50)*rotz(pi/2)*Extrusion([Vec3(0,0),Vec3(100,0),
                                           Vec3(30,0),Vec3(50,50),Vec3(70,0),Vec3(100,0),
                                           Vec3(100,100),Vec3(0,100)],Vec3(0,0,100))

get_distance_of_point_line
create_geometry(cube1)
create_geometry(cube2)
exit()

create_geometry(transy(100)*scale(100)*Polyhedron5())
create_geometry(transy(100)*trans(50-10,50,10)*scale(10)*Cube())


create_geometry(transy(300)*trans(50-10,50,10)*scale(10)*Cube())
create_geometry(transy(300)*scale(100)*Polyhedron4())



# 单位cube，points[0]=Vec3(1, 0, 0)

exit()
# 测试用例1
create_geometry(scale(10)*Cube())
create_geometry(trans(1, 1, 1)*scale(3)*Cube())
create_geometry(Cone(Vec3(5, 5, 10), Vec3(5, 5, 30), 4))
create_geometry(Sphere(Vec3(5, 5, 33), 5))
create_geometry(Sphere(Vec3(5, 5, 15), 1))
create_geometry(
    trans(10)*Extrusion([Vec3(0, 2), Vec3(0, 4), Vec3(-2, 2)], Vec3(0, 0, 5)))
create_geometry(
    trans(10)*Extrusion([Vec3(0, 2), Vec3(12, 2), Vec3(0, 8)], Vec3(0, 0, 5)))
