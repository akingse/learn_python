import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
import xml.etree.ElementTree as ET

# 读取xml
def _read_xml_mesh_inter_part(tree):
    # tree = ET.parse('文件路径')
    root = tree.getroot()
    vertexA = []
    vertexB = []
    triangleA = []
    triangleB = []
    for clashpoint in root.iter('clashpoint'):
        vector = clashpoint.find('Vector3d')
        if (not vector is None):
            if (vector.get('VAx')):
                x = float(vector.get('VAx')) 
                y = float(vector.get('VAy'))
                z = float(vector.get('VAz'))
                vertexA.append(Vec3(x, y, z))
            if (vector.get('VBx')):
                x = float(vector.get('VBx')) 
                y = float(vector.get('VBy'))
                z = float(vector.get('VBz'))
                vertexB.append(Vec3(x, y, z))
        # get face
        triA = clashpoint.find('triangleA')
        if (not triA is None):
            triangleA.append([Vec3(float(triA.get('TA0x')),float(triA.get('TA0y')),float(triA.get('TA0z'))),
                              Vec3(float(triA.get('TA1x')),float(triA.get('TA1y')),float(triA.get('TA1z'))),
                              Vec3(float(triA.get('TA2x')),float(triA.get('TA2y')),float(triA.get('TA2z')))])
        triB = clashpoint.find('triangleB')
        if (not triB is None):
            triangleB.append([Vec3(float(triB.get('TB0x')),float(triB.get('TB0y')),float(triB.get('TB0z'))),
                              Vec3(float(triB.get('TB1x')),float(triB.get('TB1y')),float(triB.get('TB1z'))),
                              Vec3(float(triB.get('TB2x')),float(triB.get('TB2y')),float(triB.get('TB2z')))])
    # show_points_line(vertexA)
    # show_points_line(vertexB)
    R=2
    ori=Vec3() #vertexA[0]
    for iter in triangleA:
        create_geometry(trans(-ori)*Section(iter).colorRed())
    for iter in triangleB:
        create_geometry(trans(-ori)*Section(iter).colorGreen())

    for iter in vertexA:
        create_geometry(trans(-ori)*Sphere(iter,R).colorRed())
    for iter in vertexB:
        create_geometry(trans(-ori)*Sphere(iter,R).colorGreen())
    return (vertexA,vertexB,triangleA,triangleB)

# 绘制两个Mesh-parts
# tree = ET.parse(r'C:\Users\Aking\source\repos\bimbase\src\xml_file\p3d.xml')
tree = ET.parse(r'C:\Users\Aking\source\repos\bimbase\src\xml_file\test_depth_debug.xml')
# mesh=_read_xml_mesh_inter_part(tree)

trigon=[
    Vec3(-52571.846922390359, 200137.84651690206, 3999.9999999999682),
    Vec3(-52571.846922390359, 200137.84651690206, -300.00000000003018),
    Vec3(-52911.066160852926, 199925.87881120876, 3999.9999999999682),
    ]
# point=mesh[0][0]
# create_geometry(Sphere(point,2).colorRed())
# create_geometry(Section(trigon).colorGreen())

triA=[
    Vec3(-3104.3029002511553, 203615.26133667614, -1.2996778653295850e-11),
    Vec3(-3286.9535856740031, 203476.36577477955, -1.2977752206211335e-11),
    Vec3(-2947.7343472114298, 203688.33348047285, -1.3011058896950091e-11),
    ]
triB=[
    Vec3(-3081.5417249541943, 203579.95860459140, -300.00000000001290),
    Vec3(-3092.6700295030910, 203597.76761461070, -300.00000000001290),
    Vec3(-3092.6700295030919, 203597.76761461070, 3999.9999999999854),
    ]
# pA=Vec3(-3092.6700295031005,203597.76761461073,-1.2996828194797176e-11)
# 求交点，精度问题
triA_0 = Vec3(-55.399210025229877, 412.29143285669988, 8.9812601800076663e-12)
triA_1 = Vec3(-200.83963971272988, 321.41032934107488, 8.9812601800076663e-12)
triA_2 = Vec3(127.25166888102012, 551.18694066919988, 8.9812601800076663e-12)
triB_0 = Vec3(127.25138376062023, 551.18688874390000, 4300.0000000000036)
triB_1 = Vec3(138.37980172937023, 533.37805085327500, 3.9790393202565610e-12)
triB_2 = Vec3(127.25138376062023, 551.18688874390000, 3.9790393202565610e-12)
triA = [triA_0, triA_1, triA_2]
triB = [triB_0, triB_1, triB_2]

pI0=Vec3(-9291.4277600683745, 5001.5715320168483, -2.1666632282407113e-12)
pI1=Vec3(-9288.7473802944405, 4992.2239368782512, -2.1659258382009720e-12)
bl=isTwoTrianglesIntersectSAT(triA,triB)
pint=getTwoTrianglesIntersectPoints(triA,triB)
# create_geometry(scale(1000)*Section(triA).colorRed())
# create_geometry(scale(1000)*Section(triB).colorGreen())
# create_geometry(Sphere(pint[0],1).colorBlue())
# create_geometry(Sphere(pint[1],1).colorBlue())


# 分离轴判断两个三角形intrusive
triA_0 = Vec3(0,0)
triA_1 = Vec3(10,0)
triA_2 = Vec3(10,10)
triB_0 = Vec3(8,0,-1)
triB_1 = Vec3(8,10,-1)
triB_2 = Vec3(8,0,10)
triA = [triA_0, triA_1, triA_2]
triB = [triB_0, triB_1, triB_2]
# create_geometry(scale(10)*Section(triA).colorRed())
# create_geometry(scale(10)*Section(triB).colorGreen())
relation=getRelationOfTwoTrianglesSAT(triA,triB)

exit()
# ------------------------------------------------------------------------------------
#  金鼓郡
# ------------------------------------------------------------------------------------

# 原生p3d
# d=0
# <summary total="4074" new="4074" active="0" reviewed="0" approved="0" resolved="0">
# + 0) 4010
# + 1) 4010
# + 1e-2) 4010
# + 1e-6) 4010

# jingujun,转自naviswork
# d=0
# <summary total="3612" new="3612" active="0" reviewed="0" approved="0" resolved="0">  # navisworks=
# d=1/1000
# <summary total="3767" new="3767" active="0" reviewed="0" approved="0" resolved="0">
# d=10/1000
# <summary total="3799" new="3799" active="0" reviewed="0" approved="0" resolved="0">
# d=100/1000
# <summary total="6401" new="6401" active="0" reviewed="0" approved="0" resolved="0">
# d=1000/1000
# <summary total="32386" new="32386" active="0" reviewed="0" approved="0" resolved="0">


# 简化测试 ---------------------
# 使用_getTriangleBoundingCircle //jingujun,转自naviswork
# + 1) 3612 total
# + 1e-1) 3605
# + 1e-2) 3555
# + 1e-3) 3554
# + 1e-6) 3554
# + 0) 3554

# 金鼓郡，lite430-p3d
count_boxA = 1852700
count_boxB = 1023029
TIT = (count_boxA+count_boxB)*12  # 34508748, 实际29269473，pointInBox

# 无优化0/1 4074/5160
# <linkage count_caltime0="0.005000s" count_caltime1="1.177000s" count_caltime2="3.275000s"/>
# <linkage count_caltime0="0.004000s" count_caltime1="1.158000s" count_caltime2="6.311000s"/>
# 优化hard 0/1 4010/5096
# <linkage count_caltime0="0.006000s" count_caltime1="1.219000s" count_caltime2="1.367000s"/>
# <linkage count_caltime0="0.004000s" count_caltime1="1.150000s" count_caltime2="5.288000s"/>
# 软碰撞优化
# <linkage count_clash_hard="4010" count_clash_soft="1421"/>
#

# world_bounding
min=(4922894.8119346518, -394596.74470618460, -713.30000000003395)
max=(4960072.4308131514, -373195.18308180763, 25620.8149999999150)


