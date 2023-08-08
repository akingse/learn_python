import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
DBL_EPSILON=2.2204460492503131e-016

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
triA_0 = Vec3(4948589.10216887, -378091.689488313, 39.9821543184115)
triA_1 = Vec3(4948589.10216887, -378102.108378973, 39.9821543184115)
triA_2 = Vec3(4948581.52809739, -378091.562127208, 39.9821426242490)
triB_0 = Vec3(4948648.64640146, -378096.898933644, 39.9822462529783)
triB_1 = Vec3(4948590.11470598, -378087.628423812, 39.9821558816473)
triB_2 = Vec3(4948588.64640146, -378096.898933644, 39.9821536146255)

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

triA_0 = Vec3(50,350,10)
triA_2 = Vec3(40,350,10)
triA_1 = Vec3(40,360,10)
triB_0 = Vec3(100,300,0)
triB_1 = Vec3(50,400,0)
triB_2 = Vec3(50,350,100)

# 精度误差, 只差一点点
triA_0 = Vec3(4935006.8329658089, -380736.84932281438, -187.97918471982871)
triA_2 = Vec3(4935010.5181025816, -380736.84932266374, -193.49438164979352)
triA_1 = Vec3(4935011.8121505287, -380736.84932261088, -200.00000000000006)
triB_0 = Vec3(4935011.0756064961, -380736.84932264080, -183.73654403252533)
triB_1 = Vec3(4935016.0613797763, -380736.84932243708, -191.19828105541887)
triB_2 = Vec3(4935009.9033790659, -380736.84932268877, -192.73244736959683)

# 三角形距离SAT
triA_0 = Vec3(-9654.0000000000000, -1033.0000000000000, 14718.000000000000)
triA_2 = Vec3(-12835.000000000000, -3760.0000000000000, 3571.0000000000000)
triA_1 = Vec3(-4543.0000000000000, -9007.0000000000000, 9925.0000000000000)
triB_0 = Vec3(7987.0000000000000, -1377.0000000000000, 8010.0000000000000)
triB_1 = Vec3(3246.0000000000000, 7701.0000000000000, 2373.0000000000000)
triB_2 = Vec3(-11417.000000000000, -2452.0000000000000, 561.00000000000000)
triA = [triA_0, triA_1, triA_2]
triB = [triB_0, triB_1, triB_2]
pointA=Vec3(-16251.912287655929, -1597.8510885997757, 952.68588087725811)
pointB=Vec3(-15447.826816046789, -2675.3116278731345, -986.39378235067693)
lineP_AB=[pointA, pointB]
mat=get_matrix_from_two_points(triA_1, triA_2)
mat=get_matrix_from_two_points(triB_2, triB_0)
segmA=[triA_1, triA_2]
segmB=[triB_2, triB_0]
vectA = segmA[1] - segmA[0]
vectB = segmB[1] - segmB[0]
vectZ = vectA.cross(vectB).normalized()
d_P2L = (segmA[0] - segmB[0] + (vectA.dot(segmB[0] - segmA[0]) / vectA.dot(vectA)) * vectA).norm()
d_P2L = get_distance_of_point_line(segmB[0],Segment(segmA[0],segmA[1]))
# d_P2L=(pointA-pointB).norm()
if (vectZ.dot(segmA[0]) < vectZ.dot(segmB[0])):
    d_P2L = -d_P2L
segmB_move = [ segmB[0] + d_P2L * vectZ, segmB[1] + d_P2L * vectZ ]

# show_points_line(segmA)
# show_points_line(segmB)
# show_points_line(segmB_move)
# show_points_line(lineP_AB)
# create_geometry(Section(triA).colorRed())
# create_geometry(Section(triB).colorGreen())
# p=Vec3(200.00000000000000, -173.20508075688772, 0.0000000000000000)
# create_geometry(trans(p)*Sphere())

# clear_entity()
# create_geometry(Section(triA0,triA1,triA2))
# create_geometry(Section(triB0,triB1,triB2))

# res=is_two_triangles_bounding_box_intersect([triA_0,triA_1,triA_2],[triB_0,triB_1,triB_2],0.001)
res = isTwoTrianglesIntersectSAT(triA, triB)
# print(res)
res = isSegmentAndTriangleIntersctSAT([triA_0, triA_1], triB)
# print(res)

triA_0 = Vec3(50,-72,0)
triA_2 = Vec3(37,21,0)
triA_1 = Vec3(0,87,0)
triB_0 = Vec3(-2,-65,0)
triB_1 = Vec3(88,16,0)
triB_2 = Vec3(24,67,0)

triA_0 = Vec3(0, 0, 0)
triA_1 = Vec3(10, 5, 0)
triA_2 = Vec3(0, 10, 0)
triB_0 = Vec3(3, 0, 0)
triB_1 = Vec3(3, 10, 0)
triB_2 = Vec3(-2, 5, 0)

triA_0 = Vec3(83.0, -88.0, 53.0)
triA_1 = Vec3(37.0, 78.0, 93.0)
triA_2 = Vec3(-93.0, -83.0, -4.0)
triB_0 = Vec3(-15.0, -4.0, 95.0)
triB_1 = Vec3(79.0, 77.0, 56.0)
triB_2 = Vec3(1.0, -49.0, -12.0)

triA_0 = Vec3(4934979.7209219905, -380736.84932392224, -192.73244736959688)
triA_1 = Vec3(4934971.8121505287, -380736.84932424547, -199.99999999981586)
triA_2 = Vec3(4934973.5629212800, -380736.84932417388, -191.19828105541882)
triB_0 = Vec3(4935011.8121505287, -380736.84932261088, -200.00000000000006)
triB_1 = Vec3(4934982.7913352484, -380736.84932379692, -187.97918471982877)
triB_2 = Vec3(4934979.1061984757, -380736.84932394756, -193.49438164979355)

triA = [triA_0, triA_1, triA_2]
triB = [triB_0, triB_1, triB_2]
# res=isPointInTriangle(g_axisNaN,triA)
res=isTwoTrianglesIntersectSAT(triA,triB)
# create_geometry(Section(triA).colorBlue())
# create_geometry(Section(triB).colorGreen())

# pnts=getTwoTrianglesIntersectPoints(triA,triB)
# show_points_line(pnts)
# res = isPointInTriangle(pnts[0],triA)
# res = isPointInTriangle(pnts[1],triA)
# res = isPointInTriangle(pnts[0],triB)
# res = isPointInTriangle(pnts[1],triB)


boxA_0 = Vec3(34.0, 7.0, 0.0)
boxA_1 = Vec3(125.0, 84.0, 71.0)
triB_0 = Vec3(73.0, -17.0, 0.0)
triB_1 = Vec3(63.0, -25.0, 0.0)
triB_2 = Vec3(8.0, -69.0, 0.0)
box=[boxA_0, boxA_1]
triB = [triB_0, triB_1, triB_2]
# create_bounding_box(box)
# create_geometry(Section(triB).colorGreen())

# 测试交点的精度
for i in range(0):
    # triA_0 = scale(randint(0,100))*Vec3(0, 0, 10)
    # triA_1 = scale(randint(0,100))*Vec3(10, 5, 0)
    # triA_2 = scale(randint(0,100))*Vec3(0, 10, 0)
    triA_0 = scale(random())*Vec3(1, 2, 10)
    triA_1 = scale(random())*Vec3(10, 5, 1)
    triA_2 = scale(random())*Vec3(3, 10, 3)
    triA = [triA_0, triA_1, triA_2]
    create_geometry(Section(triA).colorBlue())
    line=scale(random())*[Vec3(-1, -2, -10),Vec3(11, 12, 13)]
    # line=Line([Vec3(0, 0, -10),Vec3(10, 10, 10)])
    create_geometry(Line(line))
    point=getIntersectOfSegmentAndPlaneINF(line,triA)
    normalA = (triA[1] - triA[0]).cross(triA[2] - triA[0]).normalized()
    isOn1=(point-triA[0]).dot(normalA) #1.0269562977782698e-15
    isOnP=(point-triA[0]).normalized().dot(normalA) # 1.457167719820518e-16
    isOnb=fabs(isOnP)<DBL_EPSILON
    # show_points_line([point],1)
    print('return 0')

# 面接触
triA_0 = Vec3(0, 0, 0)
triA_1 = Vec3(10, 5, 0)# Vec3(10, 5, 0.000001) #相对值和设置的eps有关
triA_2 = Vec3(0, 10, 0)
# triB_0 = Vec3(3, 0, 0)
# triB_1 = Vec3(3, 10, 0)
# triB_2 = Vec3(-2, 5, 0)
triB_0 = Vec3(0, 0, 0)
triB_1 = Vec3(10, 5, 0)
triB_2 = Vec3(10, -5, 0)

triA = [triA_0, triA_1, triA_2]
# triB = trans(5,2.5)*scale(0.6)*[triB_0, triB_1, triB_2]
triB = trans(2.5,1.25)*scale(0.6)*[triB_0, triB_1, triB_2]

# 线接触
triA_0 = Vec3(0, 0, 0)
triA_1 = Vec3(10, 5, 0)
triA_2 = Vec3(0, 10, 0)
triB_0 = Vec3(5, 2.5, -10)
triB_1 = Vec3(5, 2.5, 10) #Vec3(5, 2.5, 1e8)共线判断必须单位化，否则精度的影响是致命的
triB_2 = Vec3(10, 0, 0)
# triA = rotate_arbitrary(g_axisO,Vec3(1,1,1),pi/6)*[triA_0, triA_1, triA_2]
# triB = rotate_arbitrary(g_axisO,Vec3(1,1,1),pi/6)*[triB_0, triB_1, triB_2]


# 点接触
# triB=trans(5, 2.5)*trans(0,-10)*triA
# triB=rotate_arbitrary(Vec3(5, 2.5),Vec3(1,2), -pi/6)*triB
r=random()
triA = scale(1e5)*scale(r)*[triA_0, triA_1, triA_2]
triB = scale(1e5)*scale(r)*[triB_0, triB_1, triB_2]

triA = rotate_arbitrary(g_axisX,Vec3(1,1,1),pi/6)*triA
triB = rotate_arbitrary(g_axisX,Vec3(1,1,1),pi/6)*triB

# error data
triA_0 = Vec3(0.0893163974770409, -0.3333333333333333, 0.24401693585629242)
triA_1 = Vec3(208238.36291858187, 208237.94026885106, -20422.97691672161)
triA_2 = Vec3(-64429.05675845014, 240452.51330627486, 88012.09429931616)
triB_0 = Vec3(16107.37583510938, 168547.94954260648, -250664.2130895011)
triB_1 = Vec3(192131.07639986995, 39689.65739291125, 230241.4801897153)
triB_2 = Vec3(240452.93595600568, 88011.51694904697, -64428.90205791176)
triA = [triA_0, triA_1, triA_2]
triB = [triB_0, triB_1, triB_2]
create_geometry(Section(triA).colorBlue())
create_geometry(Section(triB).colorGreen())

isOnP=isTwoIntersectTrianglesCoplanar(triA,triB)
isInter=isTwoTrianglesIntersectSAT(triA,triB)
if isInter:
    points=getTwoTrianglesIntersectPoints(triA,triB)
    isCoin=(points[1].normalized()-points[0].normalized()).isZero() #compensating error
    show_points_line(points)
    if not isCoin:
        printTrianglePair(triA,triB)

print('return 0')

