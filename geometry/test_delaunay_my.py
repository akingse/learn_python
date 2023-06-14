from shapely.geometry import Point
import sys
import os
import random
import numpy as np
mypath = 'D:\Alluser\learn_python'  # include pyp3d
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *  # NOQA: E402
from random import *  # NOQA: E402
# 集合


# numpy向量点乘和叉乘
v1 = np.array([1, 2, 3.])
v2 = np.array([2, 2, 3.])
v3 = v2-v1
sdD = np.dot(v1, v2)
print(type(sdD))
print(sdD)
sdC = np.cross(v1, v2)

a = np.mat([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
a = np.mat([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
r = GeTransform()._mat
p1 = Point(1, 2, 3)
# a = np.mat(r)
# print(a.diagonal())
# d = np.linalg.det(a)
# print(d)



def _show_close_line(points: list):
    if len(points) == 0:
        return
    points.append(points[0])
    create_geometry(Line(points))
    return points


def _is_point_in_triangle(point, trigon: list) -> bool:
    pA = trigon[0]
    pB = trigon[1]
    pC = trigon[2]
    sdA = cross(point-pA, pB-pA)
    sdB = cross(point-pB, pC-pB)
    sdC = cross(point-pC, pA-pC)

    # dAB=dot(sdA, sdB)
    # dAC=dot(sdA, sdC)
    # same direction
    # r1 = abs(norm(sdA)*norm(sdB)-dot(sdA, sdB))
    # r2 = abs(norm(sdA)*norm(sdC)-dot(sdA, sdC))
    return abs(norm(sdA)*norm(sdB)-dot(sdA, sdB)) < PL_A and abs(norm(sdA)*norm(sdC)-dot(sdA, sdC)) < PL_A
    # return abs(norm_2(sdA)*norm_2(sdB)-dAB*dAB) < PL_A and abs(norm_2(sdA)*norm_2(sdC)-dAC*dAC) < PL_A


def _is_point_in_triangle1(point, trigon: list) -> bool:
    pO = np.array([point.x, point.y, point.z])
    pA = np.array([trigon[0].x, trigon[0].y, trigon[0].z])
    pB = np.array([trigon[1].x, trigon[1].y, trigon[1].z])
    pC = np.array([trigon[2].x, trigon[2].y, trigon[2].z])
    sdA = np.cross(pO-pA, pB-pA)
    sdB = np.cross(pO-pB, pC-pB)
    sdC = np.cross(pO-pC, pA-pC)
    # same direction
    # r1 = abs(norm(sdA)*norm(sdB)-dot(sdA, sdB))
    # r2 = abs(norm(sdA)*norm(sdC)-dot(sdA, sdC))
    return abs(np.linalg.norm(sdA)*np.linalg.norm(sdB)-np.dot(sdA, sdB)) < PL_A and \
        abs(np.linalg.norm(sdA)*np.linalg.norm(sdC)-np.dot(sdA, sdC)) < PL_A


def _is_point_in_triangle2(point, trigon: list) -> bool:
    pA = trigon[0]
    pB = trigon[1]
    pC = trigon[2]
    matAB = np.mat([[pA.x, pA.y, 1], [pB.x, pB.y, 1], [point.x, point.y, 1]])
    matBC = np.mat([[pB.x, pB.y, 1], [pC.x, pC.y, 1], [point.x, point.y, 1]])
    matCA = np.mat([[pC.x, pC.y, 1], [pA.x, pA.y, 1], [point.x, point.y, 1]])
    return np.linalg.det(matAB) <= 0 and np.linalg.det(matBC) <= 0 and np.linalg.det(matCA) <= 0


def _get_circumcircle_center1(trigon: list) -> GeVec3d:
    point1 = (trigon[0])  # points cannot collinear
    point2 = (trigon[1])
    point3 = (trigon[2])
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x3, y3 = point3.x, point3.y
    k1 = (2*(x3-x2)*(y3-y1)-2*(x3-x1)*(y3-y2))
    k2 = (2*(y3-y2)*(x3-x1)-2*(y3-y1)*(x3-x2))
    if (k1 == 0 or k2 == 0):
        return g_axisNaN
    yc = ((x3-x2)*(x3**2+y3**2-x1**2-y1**2) -
          (x3-x1)*(x3**2+y3 ** 2-x2**2-y2**2)) / k1
    xc = ((y3-y2)*(x3**2+y3**2-x1**2-y1**2) -
          (y3-y1)*(x3**2+y3 ** 2-x2**2-y2**2)) / k2
    pointC = GeVec3d(xc, yc)
    return pointC


def _get_circumcircle_center(trigon: list, point: GeVec3d = GeVec3d()) -> GeVec3d:
    # _inverse_2x2
    x1, y1 = trigon[0].x, trigon[0].y
    x2, y2 = trigon[1].x, trigon[1].y
    x3, y3 = trigon[2].x, trigon[2].y
    m1 = 2*(x2-x1)
    n1 = 2*(y2-y1)
    k1 = x2*x2-x1*x1+y2*y2-y1*y1
    m2 = 2*(x3-x1)
    n2 = 2*(y3-y1)
    k2 = x3*x3-x1*x1+y3*y3-y1*y1
    k = (m1*n2-n1*m2)
    if (k == 0):  # is_float_zero(k)
        return g_axisNaN
    pointC = GeVec3d((n2*k1-n1*k2)/k, (-m2*k1+m1*k2)/k)
    return pointC
    # pointC = GeVec3d(1/k*dot(GeVec3d(n2, -n1), GeVec3d(k1, k2)),
    #                  1/k*dot(GeVec3d(-m2, m1), GeVec3d(k1, k2)))
    # return norm_2(trigon[0]-pointC) < norm_2(point-pointC)
    # return trans(pointC)*scale(norm(pointC-trigon[0]))

def _is_point_in_circumcircle0(point, trigon: list) -> bool:
    # 函数调用，对象传递约增加20%耗时
    # pointC=_get_circumcircle_center(trigon)
    x1, y1 = trigon[0].x, trigon[0].y
    x2, y2 = trigon[1].x, trigon[1].y
    x3, y3 = trigon[2].x, trigon[2].y
    m1 = 2*(x2-x1)
    n1 = 2*(y2-y1)
    k1 = x2*x2-x1*x1+y2*y2-y1*y1
    m2 = 2*(x3-x1)
    n2 = 2*(y3-y1)
    k2 = x3*x3-x1*x1+y3*y3-y1*y1
    k = (m1*n2-n1*m2)
    if (k == 0):  # is_float_zero(k)
        return g_axisNaN
    pointC = GeVec3d((n2*k1-n1*k2)/k, (-m2*k1+m1*k2)/k)
    return norm_2(trigon[0]-pointC) < norm_2(point-pointC)

def _is_point_in_circumcircle(pO, trigon: list) -> bool:
    pA = trigon[0]
    pB = trigon[1]
    pC = trigon[2]
    M = np.mat([[pA.x, pA.y, pA.x*pA.x+pA.y*pA.y, 1.0],
                [pB.x, pB.y, pB.x*pB.x+pB.y*pB.y, 1.0],
                [pC.x, pC.y, pC.x*pC.x+pC.y*pC.y, 1.0],
                [pO.x, pO.y, pO.x*pO.x+pO.y*pO.y, 1.0]])
    return np.linalg.det(M) <= 0


RP = get_rand_point
# GP = gen_rand_point

if __name__ == '__main__':
    for i in range(int(1e2)):
        # print(randint(-100, 100))
        # print(uniform(-100, 100))
        # print(random())
        pass

    tri = [Vec2(100, 0), Vec2(0, 100), Vec2(-100, -100), ]
    # res = _is_point_in_triangle(Vec2(100, 0), tri)
    res = _is_point_in_triangle2(Vec2(100, 100), tri)

    tri = [RP(), RP(), RP()]
    res = _is_point_in_triangle(RP(), tri)
    arc = get_arc_from_three_points(tri)
    # arc = arc[0]*Arc()
    # arc = _get_circumcircle_center(tri)*Arc()
    # create_geometry(arc)
    _show_close_line(tri)
    res = _is_point_in_circumcircle(Vec2(), tri)
    print('is_in_circle', res)

    tStart = time.time()
    print(time.asctime(time.localtime(tStart)))
    for i in range(int(1e5)):
        # spent time: 2.179699659347534
        # res = _is_point_in_triangle(RP(), [RP(), RP(), RP()])
        # res = _is_point_in_triangle1(RP(), [RP(), RP(), RP()])
        # res = _is_point_in_triangle1(GP(), [GP(), GP(), GP()])

        # res = _get_circumcircle_center([RP(), RP(), RP()])
        # res = _is_point_in_circumcircle0(RP(),[RP(), RP(), RP()])
        # res = _get_circumcircle_center1([RP(), RP(), RP()])
        res = _is_point_in_circumcircle(RP(),[RP(), RP(), RP()])
        pass
    print(time.time()-tStart)
    # create_geometry(scale(100)*Arc())



'''
/*
 * ┌───┐   ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┬───┐ ┌───┬───┬───┐
 * │Esc│   │ F1│ F2│ F3│ F4│ │ F5│ F6│ F7│ F8│ │ F9│F10│F11│F12│ │P/S│S L│P/B│
 * └───┘   └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┴───┘ └───┴───┴───┘
 * ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───────┐ ┌───┬───┬───┐
 * │~ `│! 1│@ 2│# 3│$ 4│% 5│^ 6│& 7│* 8│( 9│) 0│_ -│+ =│ BacSp │ │Ins│Hom│PUp│
 * ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┤ ├───┼───┼───┤
 * │ Tab │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │{ [│} ]│ | \ │ │Del│End│PDn│
 * ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴─────┤ └───┴───┴───┘
 * │ Caps │ A │ S │ D │ F │ G │ H │ J │ K │ L │: ;│" '│ Enter  │              
 * ├──────┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴────────┤     ┌───┐    
 * │ Shift  │ Z │ X │ C │ V │ B │ N │ M │< ,│> .│? /│  Shift   │     │ ↑ │    
 * ├─────┬──┴─┬─┴──┬┴───┴───┴───┴───┴───┴──┬┴───┼───┴┬────┬────┤ ┌───┼───┼───┐
 * │ Ctrl│ Wn │Alt │         Space         │ Alt│ Fn │ ME │Ctrl│ │ ← │ ↓ │ → │
 * └─────┴────┴────┴───────────────────────┴────┴────┴────┴────┘ └───┴───┴───┘
 */
'''


