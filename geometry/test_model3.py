import numpy as np
from math import *
import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402


# geo = Fusion(scale(100)*Cube(), Sweep(Section(Vec3(0, -20), scale(20)*Arc(pi)),
#                                       Line(Vec3(0, 0), Vec3(0, 0, 100))))
# create_geometry(geo)
# exit()


# filePath = r"C:\Users\Aking\Documents\WXWork\1688853868786339\Cache\File\2023-05\123.obj"
# polyface = scale(1, 1)*Polyface(filePath)
# create_geometry(polyface)
# place_to(polyface, g_matrixE)


# tri1 = [Vec3(1998.9, 734.3, 0), Vec3(
#     2998.9, 734.3, 0), Vec3(2998.9, 734.3, 3000),]
# show_points_line(tri1)
# tri2 = [Vec3(-1608.7, 1534.4, 255.1), Vec3(2488.3, -700.2, 240.5),
#         Vec3(-1625.4, 1503.2, 240.5),]
# show_points_line(tri2)


secTop = [[Segment(Vec3(0, 0), Vec3(100, 0))],
          [trans(100, 50)*rotz(-pi/2)*scale(50)*Arc(pi)],
          [SplineCurve([Vec3(100, 100), Vec3(80, 120), Vec3(0, 100)])],
          [Vec3(0, 100), Vec3(-30, 50), Vec3(0, 0)]]
secBot = transz(200)*[[Arc(pi)],
                      [Vec3(), Vec3()],
                      [],
                      []]
# create_geometry(Section(secTop))
# create_geometry(Section(secBot))

# test loft_different
arc = trans(50, 50)*scale(20)*Arc(pi/2)
sec1 = trans(0, 0, 100)*Section(arc, rotz(pi/2) * arc,
                                rotz(pi)*arc, rotz(-pi/2)*arc)
point1 = Vec3(100, 80)
point2 = Vec3(80, 100)
# roty(pi/12)*
sec2 = Section(point1, point2, rotz(pi/2)*point1, rotz(pi/2)*point2,
               rotz(pi)*point1, rotz(pi)*point2, rotz(-pi/2)*point1, rotz(-pi/2)*point2)
geo = loft_different(sec1, sec2)
# create_geometry(sec1)
# create_geometry(sec2)
# create_geometry(geo)


def _isTriangleBoundingBoxIntersect(trigon: list, box: list) -> bool:
    min = box[0]
    max = box[1]
    create_geometry(trans(min)*scale(max-min)*Cube())
    # is point in box
    pA_in = 0
    if (pA_in):
        return true

    return false


mat = roty()
# trigon=mat*[Vec3(10, 20),Vec3(80, 100),Vec3(200, 0)]
# trigon=roty(pi/2)*[Vec3(0, 0),Vec3(70, 0),Vec3(50, 100)]
# trigon = [get_rand_point(), get_rand_point(), get_rand_point()]
# trigon = [Vec3(-87, 21), Vec3(-27, -20), Vec3(-90, 95)]
# trigon = [Vec3(-10, 0), Vec3(70, 0), Vec3(50, 50)]
# trigon = [Vec3(20, 40), Vec3(200, 0), Vec3(80, 100)] #isPointInTriangle
trigon = [Vec3(20, 40), Vec3(80, 100), Vec3(200, 0)] #isPointInTriangle

create_geometry(Section(trigon))
# 测试包围圆
p, r = getTriangleBoundingCircle(trigon)
# create_geometry(trans(p)*scale(r)*Arc())
# create_geometry(trans(p)*scale(r)*Sphere())

# 测试点在三角形内
isPointInTriangle=isPointInTriangle2D
print(isPointInTriangle(mat*Vec3(0,0),trigon)) #out
print(isPointInTriangle(mat*Vec3(50,50),trigon)) #in
print(isPointInTriangle(mat*Vec3(30, 50),trigon)) #on
print(isPointInTriangle(mat*Vec3(20, 40),trigon)) #on
print(isPointInTriangle(mat*Vec3(200, 0),trigon)) #on
print(isPointInTriangle(mat*Vec3(80, 100),trigon)) #on
print(isPointInTriangle(mat*Vec3(200,100),trigon)) #out
print(isPointInTriangle(mat*Vec3(100,-20),trigon)) #out


# Nodes number in one element cube
#    5 ____________ 8
#    /            /|       z
#   /___________ / |       |
# 6|            |7 |       |____ y
#  |            |  |      /
#  |  1         |  |4    /
#  |            | /    x
#  |____________|/
# 2           3

