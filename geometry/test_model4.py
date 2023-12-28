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
        triA=[get_rand_pointF(2),get_rand_pointF(2),get_rand_pointF(2)]
        triB=[get_rand_pointF(2),get_rand_pointF(2),get_rand_pointF(2)] 
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


# 测试trigon和包围盒相交
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


# if __name__=='__main__':
#     countOut=0
    # for i in range(1000000): #100000
    #     countOut+=_use_rand_create3()
    # print('countOut=',countOut)
    # _use_rand_create1(true)

# sat必须设置共面精度
triA_0 = Vec3(-25.821536117840218, -96.71417745866091, 0.0000000000001)
triA_1 = Vec3(-58.42881123375241, -4.310362237274479, 0.0)
triA_2 = Vec3(70.29588573903484, -79.80572227527854, 0.0)
triB_0 = Vec3(5.397058792347442, -14.83335310441496, 0.0)
triB_1 = Vec3(18.301014372170044, -34.36799567085487, 0.0)
triB_2 = Vec3(36.31968900922959, 96.3960383581501, 0.0)
triA = [triA_0, triA_1, triA_2]
triB = [triB_0, triB_1, triB_2]
# create_geometry(Section(triA).colorBlue())
# create_geometry(Section(triB).colorGreen())

a=get_intersect_point_of_line_arc(Segment(Vec3(-10, 0),Vec3(0, 10)),scale(1)*Arc())

# 绘制五角星
lineList1=[100, 50, 10, 79, 65, 2, 65, 98, 10, 21]
lineList2=[98, 63, 4, 68, 77, 8, 52, 100, 19, 12]
linePnts1=[]
linePnts2=[]
for i in range(5):
    linePnts1.append(Vec3(lineList1[2*i],lineList1[2*i+1]))
    linePnts2.append(Vec3(lineList2[2*i],lineList2[2*i+1]))
# create_geometry(Section(linePnts1))
# create_geometry(Section(linePnts2))

res=isTwoTrianglesIntersectSAT(triA,triB)
a=Vec3(4929001.73, -378741.05, 0.00)
b=Vec3(4928984.49,-378757.96, 0.00)
print((a-b).norm())

# 数据过大
pointC=Vec3(509286656.03, 4458021865.35, 0.00)
k=1e10
point0=pointC+Vec3(k,0)
point1=pointC+Vec3(0,k)
arc=arc_of_center_points(pointC,point0,point1)
# create_geometry(arc)

get_intersect_point_of_two_lines
sweep_stere
print('return 0')

segm=Segment(Vec3(),Vec3())
k=3.14
point=segm.start+k*segm.vectorU

# cube1=scale(100,100,200)*Cube()
cube1=trans(-50)*Swept(Section(Vec3(-0,0),Vec3(100,0),Vec3(100,100),Vec3(0,100),),Vec3(-0,0,200))
cube2=trans(-100,-1e-6)*scale(100,100,200)*Cube()
cube3=trans(-100,-0)*scale(100,100,200)*Cube()
# create_geometry(cube1+trans(0,100)*Sphere(Vec3(-0,0),100))

cube1=scale(10000,100,100)*Cube()
prism=trans(100,-1e-3,-100)*Swept(Section(Vec3(-0,0),Vec3(5,10),Vec3(-5,10),),Vec3(0,0,1000))
create_geometry(cube1-prism)

sec=Section()
segm=Segment()
normal=get_matrixs_axisz(sec.transformation)
segmVec2=to_vec2(to_vec2(segm.vector))
mat=rotate_arbitrary(segm.start,cross(segm.vector,g_axisZ),get_angle_of_two_vectors(segmVec2,segm.vector))*\
    rotate_arbitrary(segm.start,g_axisZ,get_angle_of_two_vectors(normal,segmVec2))

is_point_in_polygon
shadow_scale_matrix

