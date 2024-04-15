import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402

# using unified function, python call c++


# 统一函数调用C++函数
def projectionPolyface(i: int):  # 在全局坐标系的原点创建一个几何体
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  "projectionPolyface")(i)
# def projectionPolyface1(i: int,show:bool=False):  # 在全局坐标系的原点创建一个几何体
#     return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  "projectionPolyface1")(i,show)

# projectionPolyface(-1) #仅遮挡算法验证show
# projectionPolyface(-1,true) 
# projectionPolyface(1) 

# for i in range(16):
#     projectionPolyface(i)
#     time.sleep(1)


def GenerateProfileArea(i: int,drawProfle:bool):  # 在全局坐标系的原点创建一个几何体
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  "GenerateProfileArea")(i,drawProfle)

def GenerateProfileDraw(i: int):  # 在全局坐标系的原点创建一个几何体
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  "GenerateProfileDraw")(i)

# GenerateProfileDraw(148)
# GenerateProfileDraw(151)

def GenerateProfileTrigon(i: int):  
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  "GenerateProfileTrigon")(i)

# GenerateProfileTrigon(17)
GenerateProfileTrigon(0)
# GenerateProfileTrigon(-1)

def testClipperFeatrueFunction(i: int):  # mdp精度对clipper的影响
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  "testClipperFeatrueFunction")(i)

# 两共线三角面，mdp=8x，mdp=6x，mdp=7v
# testClipperFeatrueFunction(8) # max=14

def GenerateProfileDebug(i: int):  
    return UnifiedFunction(PARACMPT_PARAMETRIC_COMPONENT,  "projectionPolyfaceToGenerateProfileD")(i)

# GenerateProfileDebug(8)

(-8447.6939391699998, 1504.5572337500000)
(-8447.6939391699998, 1504.5572337400001)

# 16-17
# triangle
# (56213.399798845843, 14084.321435249987)
(56194.278057715841, 14184.221562699988)
(57109.864100365841, 14189.168143169987)
# poly
(56194.278057695839, 14184.221562699988)
(57109.864100365841, 14189.168143179988)

(-647.03781815022774, -7745.1191121074808)
(-742.98265718022776, -7243.9818210274807)
(-647.07629237022775, -7745.1758172474811)

# 缺口trigon
(13274767280,-69356501864)
( 3680283377,-19242772756)
(13270919858,-69362172378)

(13270919859,-69362172378)
( 3680285322,-19242782915)
(13274767281,-69356501865)


# GenerateProfileArea(3138,false)#小误差
# GenerateProfileArea(6138) #area = 56390.607480704784

# using 11101
# GenerateProfileArea(7581) # 0.067001
# GenerateProfileArea(7582) #0.053695
# GenerateProfileArea(7581,true) #方框
# GenerateProfileArea(9314,false)

# using 27006
# GenerateProfileArea(5603,true) #三角面方向问题
# GenerateProfileArea(8819,true)
# GenerateProfileArea(5602,true)
# GenerateProfileArea(104,false) 

# 公共边
(-12952019083, 165432914191)
(-13993788103, 163444313656)
# subj
(-12952019082, 165432914191)
(-13993788104, 163444313656)

# union gap

# trigon0
(6067.1126798257656, 3000.0000000000032)
(6063.2469386957655, 3.3963942769332789e-12)
(6067.1126798257656, 3.3963942769332789e-12)
# trigon1
(6067.1126798277164, 3000.0000000000036)
(6063.1953954777164, 3000.0000000000036)
(6063.1953954777164, 3.6379788070917130e-12)
(6063.2469386977164, 3.6379788070917130e-12)

# ---
(6067.1126798257656, 1.3073986337985843e-12)
(6067.1126798257656, 3000.0000000000014)
(6063.1953954757655, 3000.0000000000014)
(6063.1953954757655, 1.3073986337985843e-12)

(6076.9858879757658, 3000.0000000000014)
(6067.2425904557658, 1.3073986337985843e-12)
(6076.9858879757658, 1.3073986337985843e-12)

# 独立三角面
(57109.864100365841, 14189.168143170002)
(56194.278057715841, 14184.221562700002)
# (56213.399798845843, 14084.321435250002)

(11070.022378640000, 3829.9429540400001)
(10932.217194810000, 3829.9429540400001)
(10932.217194760000, 3875.0240450700003) #3
(10932.217194760000, 3797.1999031000000)
(11056.703171470001, 3797.1999031000000)

(22958.172884930002, -3724.5963917600002)
(22958.071694020000, -3724.5963917600002)
(22958.169270959999, -3724.6000057199999)



