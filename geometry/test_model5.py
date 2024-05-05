import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402

# 线型
from random import *  # NOQA: E402
rect=rectangle_central_symmetry(200,100)
rect=Line(rect)
color=P3DColorDef(1, 0.5, 0.5, 1.0)
rect.symbology(color,100,0)
# create_geometry(rect)

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
get_intersect_line_of_two_planes

# cross
vec1=Vec3(-1,0,0)
vec2=Vec3(0,-1,0)
vecR=Vec3(1,1,0)

cp1=vec1.cross(vecR)
cp2=vec1.cross(vec2)
cp3=vecR.cross(vec2)

inverse
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

# 点在三角形内部
trion=[
    Vec2(-1,-1),
    Vec2(100,1),
    Vec2(1,-1),
]

# trion.reverse()
point=Vec2(0.1,0.1)
a=(trion[1]-trion[0]).dot(point-trion[0])
b=(trion[2]-trion[1]).dot(point-trion[1])
c=(trion[0]-trion[2]).dot(point-trion[2])


v1=Vec3(100,0)
v2=Vec3(100,0.001)
angle1=v1.cross(v2).z/v1.norm()/v2.norm()
angle2=v1.cross(-v2).z/v1.norm()/v2.norm()

def _getToleAngle(v1,v2):
    cr=abs(v1.cross(v2).z)
    angle=abs(v1.cross(v2).z)/v1.norm()/v2.norm()
    inTole=angle<pi/180
    return inTole


vec1=Vec3(54799.999999985812, 16875.000000000000)
vec2=Vec3(54799.999999986409, 17275.000000000000)
vec3=Vec3(54799.999999985812, 17275.000000000000)
vec1=Vec3(-669.69638095000005, 6424.8829120299997)
vec2=Vec3(-669.69638095000005, 6424.8829115999997)
vec3=Vec3(-669.11337667999999, 6400.0000000000000)

vec=Vec3(23824.999998520001, 7113.2352941800000)
vec=Vec3(23824.999998510000, 7113.2352941899999)
vec=Vec3(23824.999998510000, 7100.0000000000000)
vec=Vec3(23824.999998520001, 7100.0000000000000)

# 顺序问题
vec1=Vec3(53.438467760000002, 26.436471539999999)
vec2=Vec3(58.132393220000004, 64.754230460000002)
vec3=Vec3(56.465085870000003, 72.257113540000006)
area=3933.471977,3937486
area=3933.471977,9833390

vec1=Vec3(534384.67763689999, 264364.71540329000)
vec2=Vec3(581323.93231264001, 647542.30459307006)
vec3=Vec3(564650.85875416000, 722571.13560624002)


# _getToleAngle(vec3-vec2,vec2-vec1)
vecB1=Vec3(101.96152422706632, -7.5364438016821212e-15)
vecB2=Vec3(50.000000000000000, 49.497474683058314)
# vec3=Vec3(50.000000000000000, -21.213203435596430)
# {101.96152422706632, 70.710678118654727} 
vec1=Vec3(101.96152423000001, 0.0000000000000000)
vec2=Vec3(74.361846459999995, 26.290882939999999)
# 逐次布尔减，由于精度问题，会出现回头线
{74.361846459999995, 26.290882939999999}
{74.361846470000003, 26.290882939999999}
DBL_MAX
j=(vecB2-vecB1).cross(vec2-vecB1)

# create_geometry(scale(100)*Sphere())
# create_geometry(trans(200,0)*scale(100)*Cube())

# bug测试
# 面积异常
triA_1 = Vec3(10.0, 10.0, 0)
triA_0 = Vec3(10.0, -10.0, 0)
triA_2 = Vec3(0.0, 0.0, -0)
trigon = ( triA_0, triA_1, triA_2 )
triA_1=Vec2(-349.99999999999955, 14250.000000000000)
triA_0=Vec2(-349.99999999978263, 17750.000000000000)
triA_2=Vec2(-350.00000000000000, 17750.000000000000)

polygon=[
Vec2(6520.36200001, 2006.3344400000),
Vec2(6520.36200001, 2006.3344600001),
Vec2(6110.67149999, 3890.9107100001),
Vec2(6110.67149999, 3890.9106900001),]
# create_geometry(Section(polygon))
# show_points_line(polygon)
triA_1=Vec2(14.938485100341, 99.999999999995723)
triA_0=Vec2(14.541403694369, 101.99999999999572)
triA_2=Vec2(09.379345416746, 101.99999999999571)
trigon=[triA_0, triA_1, triA_2]
# create_geometry(Section(trigon))
# triA_0=Vec3(-556979.21307190263, 8661.3137084989812, -31947.781616607175)
# triA_1=Vec3(-556979.21307190263, 8665.9999999999964, -31959.095325106158)
# triA_2=Vec3(-555333.50146741967, 8661.3137084989812, -31947.781616607175)
# triB_0=Vec3(-556039.21935722337, 8665.1116923648115, -31293.929648480818)
# triB_1=Vec3(-556032.14828941133, 8649.5401022646820, -35081.579657425442)
# triB_2=Vec3(-556039.21935722325, 8646.6112050148258, -35081.565351396363)

# 很小的三角面与狭长的大三角面
triA_0=Vec3(-545130.26895809209, 8625.0000000000000, -36280.232394306528)
triA_1=Vec3(-545135.00245379750, 8636.4276695296867, -36280.232394306528)
triA_2=Vec3(-545121.43012332718, 8625.0000000000000, -36276.571229071356)
triB_0=Vec3(-545121.43012332730, 2600.0000000000000, -36276.571229071356)
triB_1=Vec3(-545130.26895809209, 52880.000000000000, -36280.232394306528)
triB_2=Vec3(-545121.43012332730, 52880.000000000000, -36276.571229071356)
normalA=Vec3(-2.6031750351424943e-06, -0.92387953251127597, 0.38268343235626184)
normalB=Vec3(-2.3719311276726979e-06, -0.92387953251127353, 0.38268343235777075)
normalA=Vec3(3.6102226987226508e-05, -0.0000000000000000, 0.99999999934831452)
normalB=Vec3(-0.99999999934831452, 0.0000000000000000, 3.6102226917458051e-05)
d=-2.8925622018505237e-05

trigon59=[]
# (-8481.9712553406735, 1542.1325969243635)
(-8767.6897247666548, 0.0000000000000000)
(-8444.6157833588732, 1519.0301168721785)
# round
# (-8481.9712553000008, 1542.1325969000000)
(-8767.6897248000005, 0.0000000000000000) #[8]
(-8444.6157834000005, 1519.0301168999999) #[6]
# after union
(-8767.6897247715387, 0.0000000000000000)
(-8444.6157833615380, 1519.0301168700000)
get_matrix_from_two_points
# ---------------------------------------------------------|
trigon23=[]
(-8361.9297704215405, 1500.0000000000000)
# (-8319.7768065723394, 1504.8036798991930)
(-8445.5313397241498, 1504.8036798991927)
trigon24=[]
(-8361.9297704215405, 1500.0000000000000)
(-8445.5313397241498, 1504.8036798991927)
# (-8487.6843035733509, 1500.0000000000000)
# ---------------------------------------------------------|
# after union
(-8361.9297704199998, 1500.0000000000000)
(-8319.7768065700002, 1504.8036799000001)
(-8445.5313397200007, 1504.8036799000001)
(-8487.6843035700003, 1500.0000000000000)

# mdp=6
# (-8481.9712550000004, 1542.1325970000000)
(-8767.6897250000002, 0.0000000000000000)
(-8444.6157829999993, 1519.0301170000000)

triA_0=Vec3(-779.78549095465132, -7051.5540934684677)
triA_1=Vec3(-742.98265718465132, -7243.9818210284675)
triA_2=Vec3(-647.03781814465128, -7745.1191121184675)
# 线段求交
# T22
triA_0=Vec3(-742.98265717825677, -7243.9818210315834)
triA_1=Vec3(-647.07629236825687, -7745.1758172515838)
# middle
triB_0=Vec3(-742.98265718465132, -7243.9818210284675)
triB_1=Vec3(-647.03781814465128, -7745.1191121184675)
# 交点

area=(triA_2-triA_1).cross(triA_1-triA_0)
point=get_intersect_point_of_two_lines(Segment(triA_0,triA_1),Segment(triB_0,triB_1))
# (-742.9826459060845,  -7243.981879938467,0.0)
# (-742.98263773465135, -7243.9819226184682)

cro=normalA.cross(normalB).norm()
pd=Vec3(-9.9999999997671694, 0.0000000000000000, -6.1981547332834452e-05)
d=normalA.dot(pd)

# need repair
# triA_0=Vec3(-540421.41940188315, 11850.000000000000, -31339.051866911719)#
# triA_1=Vec3(-539771.43026757101, 11830.000000000000, -31339.075332967001)
# triA_2=Vec3(-539771.43026757101, 14800.000000000000, -31339.075332967001)
# triB_0=Vec3(-540421.41759681783, 8900.0000000000000, -31339.051866976894)#
# triB_1=Vec3(-540421.41759681783, 11850.000000000000, -31339.051866976894)
# triB_2=Vec3(-540421.35261345189, 8900.0000000000000, -29539.069665128605)


trigonA=[triA_0, triA_1, triA_2]
trigonB=[triB_0, triB_1, triB_2]
create_geometry(trans(-triA_0)*Section(trigonA).colorBlue())
create_geometry(trans(-triA_0)*Section(trigonB).colorGreen())


print('return 0')

