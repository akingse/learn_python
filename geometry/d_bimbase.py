import xml.etree.ElementTree as ET
from math import *
import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
size = 1
tree = ET.parse(r'C:\Users\Aking\source\repos\bimbase\xml_gen\p3d.xml')
geo = Combine()
segment = []


def create_bound_box(min: GeVec3d, max: GeVec3d):
    create_geometry(trans(min)*scale(max-min)*Cube().colorRed())


for clashresult in tree.getroot().find('batchtest').find('clashtests').find('clashtest').find('clashresults').findall('clashresult'):
    pos = clashresult.find('clashpoint').find('pos3f')
    # print([clashobject.find('objectattribute').find('value').text for clashobject in clashresult.find('clashobjects').findall('clashobject')])
    # print(float(pos.get('x')), float(pos.get('y')), float(pos.get('z')))
    # cube = trans(-size/2, -size/2, -size/2) * \
    #     trans(GeVec3d(float(pos.get('x')), float(pos.get('y')),
    #           float(pos.get('z')))) * scale(size) * Cube()
    # cube.color(1, 0, 0, 0.3)
    # geo.append(cube)
    segment = [GeVec3d(float(pos.get('xS')), float(pos.get('yS')), float(pos.get('zS'))),
               GeVec3d(float(pos.get('xE')), float(pos.get('yE')), float(pos.get('zE')))]
    # create_geometry(geo)
    if len(segment) == 2:
        # print(segment[0])
        # print(segment[1])
        d = norm(segment[1]-segment[0])
        if (d > PL_A):
            print('d =', d)
        # show_points_line(segment)
        # create_geometry(trans(segment[0])*scale(0.1)*Cube().colorCyan(0.1))
    else:
        print('NotOverlap')

# create_geometry(Sphere(GeVec3d(3.1415926535897931, 0.38330090700000002, 10.000000000000000)))
# create_geometry(Sphere(GeVec3d(3.1415926535897931, 0.38330090700000008, 3.1415926535897931)))

segment = [GeVec3d(-5.0000000000000000, -5.0000000000000000, -10.000000000000000),
           GeVec3d(5.0000000000000000, 5.0000000000000000, 0.0000000000000000)]
# show_points_line(segment)

# object2,boundbox
# p1 = Vec3(-5.0000000000000000, -5.5186613842545924, -10.000000000000000)
# p2 = Vec3(10.212660465455269, 10.212660465455270, 16.247448713915890)
# create_bound_box(p1, p2)

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


