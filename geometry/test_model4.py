import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
from random import *  # NOQA: E402

def _test_refer(alist):
    alist[0]=Vec3(0, 0)
    return
vecSeg=[g_axisNaN]
_test_refer(vecSeg)

triA = [Vec3(0, 0), Vec3(100, 0), Vec3(50, 100)]
triB = roty(pi/6)*trans(0, 100)*triA
triA = rotz(pi/6)*trans(200, 0, 100)*triA
# create_geometry(Section(triA).colorBlue())
# create_geometry(Section(triB).colorGreen())
# isTwoTrianglesIntersectSAT(triA, triB)
# isTwoTrianglesIntersection2D(triA, triB)

# 交叉验证
def _use_rand_create1(show=False):
    countOut=0
    isInter=False
    while (not isInter):
        triA=[get_rand_point(3),get_rand_point(3),get_rand_point(3)]
        triB=[get_rand_point(3),get_rand_point(3),get_rand_point(3)]
        triA=[get_rand_point(2),get_rand_point(2),get_rand_point(2)]
        triB=[get_rand_point(2),get_rand_point(2),get_rand_point(2)] #scale(0.1)*
        sum=0
        if (isTwoTrianglesIntersectSAT(triA,triB)):
            isInter=True
            if show:
                create_geometry(Section(triA).colorBlue())
                create_geometry(Section(triB).colorGreen())
            pnts=getTwoTrianglesIntersectPoints(triA,triB)
            if show:
                show_points_line(pnts)
            if (not pnts[0].isValid() or not pnts[1].isValid()):
                countOut+=1
                printTrianglePair(triA,triB)
            if (not isPointInTriangle(pnts[0],triA)):
                countOut+=1
                printTrianglePair(triA,triB)
            if (not isPointInTriangle(pnts[1],triA)):
                countOut+=1
                printTrianglePair(triA,triB)
            if (not isPointInTriangle(pnts[0],triB)):
                countOut+=1
                printTrianglePair(triA,triB)
            if (not isPointInTriangle(pnts[1],triB)):
                countOut+=1
                printTrianglePair(triA,triB)
            normalA=(triA[1]-triA[0]).cross(triA[2]-triA[1])
            dotPro0=normalA.dot(pnts[0]-triA[0])
            sum+=fabs(dotPro0)
            dotPro1=normalA.dot(pnts[1]-triA[0])
            sum+=fabs(dotPro1)
            normalB=(triB[1]-triB[0]).cross(triB[2]-triB[1])
            dotPro0=normalB.dot(pnts[0]-triB[0])
            sum+=fabs(dotPro0)
            dotPro1=normalB.dot(pnts[1]-triB[0])
            sum+=fabs(dotPro1)
            # print('intersect, sum=',sum)
    return countOut


def _use_rand_create2(show=False):
    countOut=0
    triA=[get_rand_point(3),get_rand_point(3),get_rand_point(3)]
    triB=[get_rand_point(3),get_rand_point(3),get_rand_point(3)]
    if (not isTwoTrianglesBoundingBoxIntersect(triA,triB) and isTwoTrianglesIntersectSAT(triA,triB)):
        countOut+=1
        printTrianglePair(triA,triB)
    return countOut


def _use_rand_create3(show=False):
    countOut=0
    # triA=[get_rand_point(2),get_rand_point(2),get_rand_point(2)]
    triA=[get_rand_point(3),get_rand_point(3),get_rand_point(3)]
    boxB=get_rand_box()
    if (isTriangleAndBoundingBoxIntersect(triA,boxB) != isTriangleAndBoundingBoxIntersectSAT(triA,boxB)):
        if (not is_parallel(triA[1]-triA[0],triA[2]-triA[0])):
            countOut+=1
            print_vector(boxB[0])
            print_vector(boxB[1])
            printTriangle(triA)
    return countOut


countOut=0
# for i in range(1000000): #100000
#     countOut+=_use_rand_create3()
# print('countOut=',countOut)
_use_rand_create1(true)

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
print('return 0')



