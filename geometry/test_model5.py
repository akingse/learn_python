import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
from random import *  # NOQA: E402


# 精度测试
segm1=[Vec3(1.1, 0.2), Vec3(12.2, 0.2)]
segm2=[Vec3(2.2,5.7), Vec3(2.2,102.2)]

segm1=roty(pi/4)*[Vec3(-2.2, 1.2), Vec3(12.2, 1.2)]
segm2=roty(pi/4)*[Vec3(2.2,5.7), Vec3(2.2,102.2)]

d1=(segm1[1]-segm1[0]).dot(segm2[1]-segm2[0])

def _getSegmentIntersect(segmA,segmB):
    # vecA=segmA[1]-segmA[0]
    m1=(segmA[0]-segmB[0]).cross(segmA[0]-segmB[1])
    m2=(segmB[0]-segmB[1]).cross(segmA[1]-segmA[0])
    k= sqrt(m1.norm2()/m2.norm2())
    return segmA[0]+k*(segmA[1]-segmA[0])

# 线段相交，叉乘
segm1=[Vec3(-5, 1), Vec3(9, 5)]
segm2=[Vec3(7, -1), Vec3(0,4)]
# show_points_line(segm1)
# show_points_line(segm2)
# point=_getSegmentIntersect(segm1,segm2)
# show_points_line([point])

a=math.inf
a=DBL_MAX

# 点在线上，误差的影响
point = rotz(pi/3)*Vec3(1.1, 1.2, -1)
trigon = rotz(pi/3)*[Vec3(0, 0), Vec3(2.2, 2.4)]
cp = (point - trigon[1]).cross(point - trigon[0])


# cross
vec1=Vec3(-1,0,0)
vec2=Vec3(0,-1,0)
vecR=Vec3(1,1,0)

cp1=vec1.cross(vecR)
cp2=vec1.cross(vec2)
cp3=vecR.cross(vec2)


# 测试交点精度
triA_0 = Vec3(10,10,0+random())
triA_1 = Vec3(10, -10, 0+random())
triA_2 = Vec3(10,0,20+random())
triB_0 = Vec3(random(),random(),random())
triB_1 = Vec3(20+random(),random(),10+random())


triA_0 = Vec3(10.0, 10.0, 0.15337962890365708)
triA_1 = Vec3(10.0, -10.0, 0.25843292414572383)
triA_2 = Vec3(10.0, 0.0, 20.9886529284422)
triB_0 = Vec3(0.07721563132876663, 0.9563725236941445, 0.7091018503950636)
triB_1 = Vec3(20.8213602646909, 0.7961723114870606, 10.681037805092565)
# (10.0, 0.8797421207712053, 5.479092224330559)

# triB_2 = Vec3()
plane = ( triA_0, triA_1, triA_2 )
segment = ( triB_0 ,triB_1 )

vecSeg = segment[1] - segment[0]
normal = (plane[1] - plane[0]).cross(plane[2] - plane[1])
k= (plane[0] - segment[0]).dot(normal) / vecSeg.dot(normal)
local = segment[0] + k * vecSeg
if (local.x!=10.0):
    printTriangle(plane)
    printTriangle([segment[0],segment[1],local])
    # print(local)

# 接近平行时的交点
triA_0 = Vec3(10.0, 10.0, 0)
triA_1 = Vec3(10.0, -10.0, 0)
triA_2 = Vec3(10.0, 0.0, -0.000000000001)
triB_0 = Vec3(-10, 0, 0)
triB_1 = Vec3(20, 0., 0.)
trigon = ( triA_0, triA_1, triA_2 )
segment = ( triB_0 ,triB_1 )
rayX=Vec3(1,0,0)
point=triB_0
normal = (trigon[1] - trigon[0]).cross(trigon[2] - trigon[0])
deno = rayX.dot(normal)
k = (trigon[0] - point).dot(normal) / deno
local = point + k * rayX

# 2D 点在三角形内
clear_entity()
triA_1 = Vec3(10.0, 10.0, 0)
triA_0 = Vec3(10.0, -10.0, 0)
triA_2 = Vec3(0.0, 0.0, -0)
trigon = ( triA_0, triA_1, triA_2 )
trigon=get_rand_triangle()
# create_geometry(Section(trigon))
point=get_rand_point(2)
point=Vec3(5.0, 6.0, -1)
# show_points_line([point],2)
res=isPointInTriangle2D(point,trigon)
print(res)

# 点在平面上方
normal = (trigon[1] - trigon[0]).cross(trigon[2] - trigon[0])
res=normal.z*normal.dot(point-trigon[0])

print('return 0')

