import numpy as np
from math import *
import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402


def isTwoTrianglesIntersection2D(triA, triB):
    pA0 = triA[0]
    pA1 = triA[1]
    pA2 = triA[2]
    pB0 = triB[0]
    pB1 = triB[1]
    pB2 = triB[2]
    vecA0 = triA[1] - triA[0]
    vecA1 = triA[2] - triA[1]
    vecA2 = triA[0] - triA[2]
    axisA0 = Vec3(-vecA0.y, vecA0.x)
    axisA1 = Vec3(-vecA1.y, vecA1.x)
    axisA2 = Vec3(-vecA2.y, vecA2.x)
    dotA0 = axisA0.dot(pA0)
    dotA1 = axisA0.dot(pA1)
    dotA2 = axisA0.dot(pA2)
    dotB0 = axisA0.dot(pB0)
    dotB1 = axisA0.dot(pB1)
    dotB2 = axisA0.dot(pB2)
    # show_points_line([Vec3(), axisA0])
    return


triA = [Vec3(0, 0), Vec3(100, 0), Vec3(50, 100)]
triB = trans(0, 100)*triA
triA = rotz(pi/6)*trans(200, 0, 100)*triA
create_geometry(Section(triA).colorBlue())
create_geometry(Section(triB).colorGreen())
isTwoTrianglesIntersection(triA, triB)

isTwoTrianglesIntersection2D(triA, triB)

# 分离轴定理，可视化