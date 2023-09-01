import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
from random import *  # NOQA: E402
DBL_EPSILON=2.2204460492503131e-016


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


print('return 0')
