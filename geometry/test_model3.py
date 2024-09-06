from math import *
import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402

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

# 函数接口测试-python version
# 三角形和包围盒相交

mat = roty()  # pi/4
# trigon=mat*[Vec3(10, 20),Vec3(80, 100),Vec3(200, 0)]
# trigon=roty(pi/2)*[Vec3(0, 0),Vec3(70, 0),Vec3(50, 100)]
# trigon = [get_rand_point(), get_rand_point(), get_rand_point()]
# trigon = [Vec3(-87, 21), Vec3(-27, -20), Vec3(-90, 95)]
# trigon = [Vec3(-10, 0), Vec3(70, 0), Vec3(50, 50)]
# trigon = [Vec3(20, 40), Vec3(200, 0), Vec3(80, 100)] #isPointInTriangle
# trigon = [Vec3(20, 40), Vec3(80, 100), Vec3(200, 0), ] #isPointInTriangle
# trigon = [Vec3(200, 0), Vec3(80, 100),Vec3(20, 40), ] #isPointInTriangle
p1 = Vec3(20, 40)
p2 = Vec3(200, 0)
p3 = Vec3(80, 100)
trigon = mat*[p3, p1, p2, ]


# create_geometry(Section(trigon))
# 测试包围圆
# p, r = getTriangleBoundingCircle(trigon)
# create_geometry(trans(p)*scale(r)*Arc())
# create_geometry(trans(p)*scale(r)*Sphere())

# 测试点在三角形内
isPointInTriangle = isPointInTriangle2D
print(isPointInTriangle(mat*Vec3(0, 0), trigon))  # out
print(isPointInTriangle(mat*Vec3(30, 80), trigon))  # out
print(isPointInTriangle(mat*Vec3(80, 120), trigon))  # out
print(isPointInTriangle(mat*Vec3(50, 50), trigon))  # in
print(isPointInTriangle(mat*Vec3(30, 50), trigon))  # on
print(isPointInTriangle(mat*Vec3(20, 40), trigon))  # on
print(isPointInTriangle(mat*Vec3(200, 0), trigon))  # on
print(isPointInTriangle(mat*Vec3(80, 100), trigon))  # on
print(isPointInTriangle(mat*Vec3(200, 100), trigon))  # out
print(isPointInTriangle(mat*Vec3(100, -20), trigon))  # out

# exit(0)
pS = Vec3(0, 0, 100)
# print(_test_fun([pS,Vec3(0,0,0)],trigon)) #out
# print(_test_fun([pS,Vec3(30,80)],trigon)) #out
# print(_test_fun([pS,Vec3(80,120)],trigon)) #out
# print(_test_fun([pS,Vec3(50,50)],trigon)) #out
# print(_test_fun([pS,Vec3(30, 50)],trigon)) #on
# print(_test_fun([pS,Vec3(20, 40)],trigon)) #on
# print(_test_fun([pS,Vec3(200, 0)],trigon)) #on
# print(_test_fun([pS,Vec3(80, 100)],trigon)) #on
# print(_test_fun([pS,Vec3(200,100)],trigon)) #out
# print(_test_fun([pS,Vec3(100,-20)],trigon)) #out

# 测试 isTwoTrianglesIntersection1
triL = [Vec3(0, 0), Vec3(100, 0), Vec3(0, 100)]
triR = [Vec3(0, 0), Vec3(100, 0), Vec3(100, 100)]
_test_fun = TrianglesIntersection_part1_
# print(_test_fun(triL,trans(200,0,1)*triL))
# print(_test_fun(triL,trans(200,0,1)*triL,rotx(pi/2)))
# print(_test_fun(triL,trans(200,0,1)*triL,rotz(pi/2)))
# print(_test_fun(triL,trans(100,0,1)*triL))
# print(_test_fun(triL,trans(100,0,1)*triL,rotx(pi/2)))
# print(_test_fun(triL,trans(100,0,1)*triL,rotz(pi/2)))
# print(_test_fun(trans(-1,0)*triL,roty(-pi/2)*triL))
# print(_test_fun(trans(-1,0)*triL,transz(10)*roty(-pi/2)*triL))
# print(_test_fun(trans(-1,0)*triL,transz(-10)*roty(-pi/2)*triL))

print('intersect')
# print(_test_fun(triL, trans()*roty(-pi/2)*triR))  # 点在面内
# print(_test_fun(triL, trans(1, 0)*roty(-pi/2)*triR))
# print(_test_fun(triL, trans(1, 1)*roty(-pi/2)*triR))
# print(_test_fun(triL, roty(-pi/2)*triL))
# print(_test_fun(triL, roty(-pi/6)*triL))
# print(_test_fun(triL, trans(100, 0)*roty(-pi/6)*triL))
# create_geometry(Section(trans(0,0)*triL).colorBlue())
# create_geometry(Section(roty(-pi/2)*triL).colorBlue())


def isPointContainedInTriangle(point, triangle):
    v0 = triangle[0]
    v1 = triangle[1]
    v2 = triangle[2]
    edge1 = v1 - v0
    edge2 = v2 - v0
    ptVec = point - v0
    normal = edge1.cross(edge2)
    normal.normalized()
    dot1 = normal.dot(edge1.cross(ptVec))
    dot2 = normal.dot(ptVec.cross(edge2))
    # is perpendi
    dotPro = normal.dot(ptVec)  # -1.0097419586828951e-28
    return (dot1 >= 0.0 and dot2 >= 0.0 and dot1 + dot2 <= normal.dot(normal))


triA_0 = Vec3(-2, 1)
triA_1 = Vec3(1, -1)
triA_2 = Vec3(1, 1)
# triB_0 = Vec3(0,0)
# triB_1 = Vec3(4,0)
# triB_2 = Vec3(2,1)
triA = scale(10)*[triA_0, triA_1, triA_2]
# create_geometry(Section(triA).colorBlue())
# show_points_line()
theta = pi/2
sk = scale(1e6)
res = isPointContainedInTriangle(
    roty(theta)*sk*Vec3(11.2, 0.2), roty(theta)*sk*triA)
print(res)
print(math.inf)

sw = scale(10)*Sweep(Section(Vec3(0, 0), Vec3(2, 0), Vec3(2, 1),
                             Vec3(1, 1), Vec3(1, 2), Vec3(0, 2)), Line(Vec3(0, 0), Vec3(0, 0, 1)))
# create_geometry(scale(10)*Line(Vec3(2,1,1),Vec3(1,1),Vec3(1,2,1)))
# create_geometry(sw)

# d=4.6566128730773926e-10
# count_pre_clash=count_clash_hard+count_clash_soft

# 改bug
# total="4074" riangularIntersectC="114014424"

# data load finish, cost time = 3.178s
TriangularIntersectC = 44420000
count_edgeCrossTri = 0
count_pointInTri = 127080000  # 由于return true会提前中止函数，所有这个数字比count_across小
count_segCrossTri = 0
count_across = 177680000
# 使用射线法
#  total="48718"， total="48698"

normal=Vec3(3.6611652351681565, 8.8388347648318444, -3.6611652351681556).normalized()
p2=Vec3(7.5000000000000000, 7.5000000000000000, 29.464466094067262)
p10=Vec3(8.5355339059327378, 8.5355339059327378, 33.000000000000000)
res=(p10-p2).normalized().dot(normal)

