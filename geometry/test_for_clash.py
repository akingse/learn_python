import sys
import os
mypath = 'D:/Alluser/learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
J2=sqrt(2)
J3=sqrt(3)
testCase = 'Overlap(cube-cube)' #相交
testCase = 'Disjoint(cube-cube)' #面平行
testCase = 'Disjoint(cone-cone)' #面平行
testCase = 'Disjoint(cone-cone)1' #圆弧到面
testCase = 'Disjoint(cube-cube)2' #点面
testCase = 'Disjoint(cube-cube)3' #线线平行
testCase = 'Disjoint(cube-cube)4' #线线平行
testCase = 'Disjoint(cube-cube)5' #点点
testCase = 'Disjoint(cube-cube)6' #点线

# 测试方法，配置clashDetective的BIMBase打开p3d，启动命令 ..，输出xml，运行python脚本读取xml并绘制图形；


if testCase == 'Overlap(cube-cube)':
    cube1=rotx(pi/3)*rotz(pi/4)*scale(10)*Cube()
    cube2=mirror_xoy()*trans(-5,-5)*scale(10)*Cube()
    # create_geometry(cube1)
    create_geometry(cube2)
    create_geometry(trans(pi,pi,-1)*cube1)
# 测试结果
# d=0
# test PASS，重合相交，返回两个重合点
# test PASS，碰撞侵入时，暂时无法计算侵入距离，目前使用求交的包围盒的center
elif testCase == 'Disjoint(cube-cube)': #d=10-pi
    cube1=rotz(pi/6)*scale(pi)*Cube()
    cube2=trans(pi/3,pi/3,10)*rotz(pi/6)*scale(pi)*Cube()
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 6.858407
# test PASS
elif testCase == 'Disjoint(cone-cone)': #d=10-pi
    cube1=rotz(pi/6)*scale(pi)*Cone()
    cube2=trans(pi/3,pi/3,10)*rotz(pi/6)*scale(pi)*Cone()
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 6.858407
# test PASS

elif testCase == 'Disjoint(cone-cone)1': #d=20-5J2
    cube1=rotz(pi/6)*scale(10)*Cone()
    cube2=trans(00,0,30)*roty(-pi/4)*rotz(pi/6)*scale(10)*Cone()
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 13.169872999999999
# test PASS，方向对了，距离和离散精度有关

elif testCase == 'Disjoint(cube-cube)2': #d=10
    cube1=rotx(pi/3)*rotz(pi/4)*scale(10)*Cube()
    cube2=mirror_xoy()*trans(-5,-5,10)*scale(10.2)*Cube()
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 10.0
# test PASS
elif testCase == 'Disjoint(cube-cube)3': #d=10*J2
    cube1=trans(10,pi/2,10)*scale(pi)*Cube()
    cube2=mirror_xoy()*mirror_yoz()*scale(pi)*Cube()
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 14.142135623730951
# test PASS
elif testCase == 'Disjoint(cube-cube)4': #d=30/*J2
    p=Vec3(10,5,20)
    cube1=rotate_arbitrary(p,Vec3(-1,0,1),-pi/6)*trans(p)*roty(pi/4)*scale(20)*Cube()
    cube2=scale(10)*Cube() #mirror_xoy()*mirror_yoz()*
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 7.0710678118654755
# test PASS
elif testCase == 'Disjoint(cube-cube)5': #d=10*J3
    cube1=scale(10)*Cube()
    cube2=trans(20,20,20)*scale(10)*Cube()
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 17.320508075688775
# test PASS

elif testCase == 'Disjoint(cube-cube)6': #d=15/J2
    cube1=scale(-10)*Cube()
    cube2=trans(10,5,0)*rotz(pi/4)*scale(10)*Cube()
    create_geometry(cube1)
    create_geometry(cube2)
# 测试结果
# d = 10.606601717798213
# test PASS

