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
trigon = mat*[p2, p1, p3, ]


# create_geometry(Section(trigon))
# 测试包围圆
# p, r = getTriangleBoundingCircle(trigon)
# create_geometry(trans(p)*scale(r)*Arc())
# create_geometry(trans(p)*scale(r)*Sphere())

# 测试点在三角形内
# isPointInTriangle=isPointInTriangle2D
# print(isPointInTriangle(mat*Vec3(0, 0), trigon))  # out
# print(isPointInTriangle(mat*Vec3(30, 80), trigon))  # out
# print(isPointInTriangle(mat*Vec3(80, 120), trigon))  # out
# print(isPointInTriangle(mat*Vec3(50, 50), trigon))  # in
# print(isPointInTriangle(mat*Vec3(30, 50), trigon))  # on
# print(isPointInTriangle(mat*Vec3(20, 40), trigon))  # on
# print(isPointInTriangle(mat*Vec3(200, 0), trigon))  # on
# print(isPointInTriangle(mat*Vec3(80, 100), trigon))  # on
# print(isPointInTriangle(mat*Vec3(200, 100), trigon))  # out
# print(isPointInTriangle(mat*Vec3(100, -20), trigon))  # out

# exit(0)
_test_fun = is_segment_cross_triangle_surface
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

# 测试三角形与包围盒相交
# res=isTriangleBoundingBoxIntersect(trigon, [Vec3(100,100,100),Vec3(700,600,500)])

triA_0 = Vec3(4924425.884660, -385631.016734, 5390.000000)
triA_1 = Vec3(4924433.371383, -385624.275658, 5390.000000)
triA_2 = Vec3(4924471.172876, -385626.256750, 5390.000000)
triB_0 = Vec3(4924425.908760, -385651.280850, 5390.000000)
triB_1 = Vec3(4924436.214129, -385631.055425, 5390.000000)
triB_2 = Vec3(4924443.183335, -385627.504437, 5390.000000)

triA_0 = Vec3(4924494.812277, -385870.182834, 5750.000000)
triA_1 = Vec3(4924599.812277, -385945.182834, 5750.000000)
triA_2 = Vec3(4924586.871325, -385946.886543, 5750.000000)
triB_0 = Vec3(4924601.810260, -385940.893598, 5750.000000)
triB_1 = Vec3(4924595.257704, -385951.321931, 5750.000000)
triB_2 = Vec3(4924589.810992, -385975.185537, 5750.000000)


triA_0 = Vec3(100, 0, 0)
triA_1 = Vec3(0, 173.205, 0)
triA_2 = Vec3(-100, 0, 0)
triB_0 = Vec3(73.2051, 0, -1.22465e-14)
triB_1 = Vec3(173.205, 173.205, 0)
triB_2 = Vec3(273.205, 0, 1.22465e-14)

# triA_0 = Vec3(4948618.646401, -378059.398934, 39.982200)
# triA_1 = Vec3(4948618.646401, -378066.898934, 39.982200)
# triA_2 = Vec3(4948608.385797, -378068.708155, 39.982184)
# triB_0 = Vec3(4948648.646401, -378096.898934, 39.982246)
# triB_1 = Vec3(4948618.646401, -378066.898934, 39.982200)
# triB_2 = Vec3(4948609.375892, -378068.367238, 39.982186)

# 相离
triA_0 = Vec3(4948589.10216887,-378091.689488313,39.9821543184115)
triA_1 = Vec3(4948589.10216887,-378102.108378973,39.9821543184115)
triA_2 = Vec3(4948581.52809739,-378091.562127208,39.9821426242490)
triB_0 = Vec3(4948648.64640146,-378096.898933644,39.9822462529783)
triB_1 = Vec3(4948590.11470598,-378087.628423812,39.9821558816473)
triB_2 = Vec3(4948588.64640146,-378096.898933644,39.9821536146255)

# triA_0 = Vec3(1,1)
# triA_1 = Vec3(-2,1-0.0001)
# triA_2 = Vec3(1,-1)
# triB_0 = Vec3(0,0)
# triB_1 = Vec3(4,0)
# triB_2 = Vec3(2,1)


# triA_0 = Vec3(4934991.08492488,-380736.849323458,-266.330042529162)
# triA_1 = Vec3(4934984.36869635,-380736.849323732,-263.095677331456)
# triA_2 = Vec3(4934986.01043158,-380736.849323665,-271.249229247876)
# triB_0 = Vec3(4934988.30653218,-380736.849323571,-265.705952052692)
# triB_1 = Vec3(4934982.79133525,-380736.849323797,-262.020815280171)
# triB_2 = Vec3(4935011.81215053,-380736.849322611,-250.000000000000)

triA_0 = Vec3(4935003.6138694724, -380736.84932294575, -221.24922924757556)
triA_2 = Vec3(4935003.6138694724, -380736.84932294575, -221.24922924757556)
triA_1 = Vec3(4934991.0849248841, -380736.84932345786, -216.33004252886147)
triB_0 = Vec3(4934988.3065321781, -380736.84932357143, -215.70595205269194)
triB_1 = Vec3(4934982.7913352484, -380736.84932379687, -212.02081528017138)
triB_2 = Vec3(4935011.8121505287, -380736.84932261088, -200.00000000000006)

# triA_0 = Vec3(2,1,1) #2D error
# triA_0 = Vec3(2,1,1)
# triA_1 = triA_0#Vec3(-2,1)
# triA_2 = Vec3(1,2,1)
# triB_0 = Vec3(0,0)
# triB_1 = Vec3(4,0)
# triB_2 = Vec3(2,1)

triA=[triA_0,triA_1,triA_2]
triB=[triB_0,triB_1,triB_2]
create_geometry(Section(triA).colorRed())
create_geometry(Section(triB).colorGreen())
# p=Vec3(200.00000000000000, -173.20508075688772, 0.0000000000000000)
# create_geometry(trans(p)*Sphere())

# clear_entity()
# create_geometry(Section(triA0,triA1,triA2))
# create_geometry(Section(triB0,triB1,triB2))

# res=is_two_triangles_bounding_box_intersect([triA_0,triA_1,triA_2],[triB_0,triB_1,triB_2],0.001)
res=isTwoTrianglesIntersectionSAT(triA,triB)
print(res)
res=isSegmentAndTriangleIntersctSAT([triA_0,triA_1],triB)
print(res)

# d=4.6566128730773926e-10
# count_pre_clash=count_clash_hard+count_clash_soft

# 改bug
# total="4074" riangularIntersectC="114014424"

is_two_line_intersect

# data load finish, cost time = 3.178s
time = 18.529
time = 18.457
time = 19.088
TriangularIntersectC = 44420000
count_edgeCrossTri = 0
count_pointInTri = 127080000  # 由于return true会提前中止函数，所有这个数字比count_across小
count_segCrossTri = 0
count_across = 177680000
