# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 矢量计算函数
# Author: akingse
# Date: 2021/12
from .pyp3d_math import *

g_axisX = GeVec3d(1, 0, 0)
g_axisY = GeVec3d(0, 1, 0)
g_axisZ = GeVec3d(0, 0, 1)
g_axisO = GeVec3d(0, 0, 0)  # coordinate original point
g_axisNaN = GeVec3d(float("nan"), float("nan"), float("nan"))
g_matrixO = GeTransform(
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])  # Zero Matrix
g_matrixE = GeTransform(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])  # Identity Matrix
g_matrixI = g_matrixE
m_pi = 3.141592653589793  # reserve 15 decimal places
m_e = 2.718281828459045
# pyp3d_data
Vec3 = GeVec3d
Vec2 = GeVec2d
# ------------------------------------------------------------------------------------------
# |                                         JUDGE                                          |
# ------------------------------------------------------------------------------------------


# def is_all_vec(points): return True if all(isinstance(
#     i, (GeVec2d, GeVec3d)) for i in points) else False
def is_all_vec(points) -> bool:
    for iter in points:
        if isinstance(iter, (GeVec2d, GeVec3d)):
            continue
        elif isinstance(iter, list):
            is_all_vec(iter)
        else:
            return False
    return True


def is_all_vec2(points) -> bool:
    return all(isinstance(i, GeVec2d) for i in points)


def is_all_vec3(points) -> bool:
    return all(isinstance(i, GeVec3d) for i in points)


def is_all_num(num) -> bool:  # 判断对象是否为数字
    '''
    judge a object is Number(int or float), using recursion
    '''
    if isinstance(num, (int, float)):
        return True
    elif isinstance(num, (list, tuple)):
        for i in num:
            if not is_all_num(i):
                return False
        return True
    else:
        return False

# ------------------------------------------------------------------------------------------
# |                                         VECTOR                                         |
# ------------------------------------------------------------------------------------------


def norm(vec) -> float:  # 计算模长（二范数）
    '''
    the absolute length of vector
    '''
    if isinstance(vec, GeVec2d):
        return sqrt(vec.x*vec.x + vec.y*vec.y)
    elif isinstance(vec, GeVec3d):
        return sqrt(vec.x*vec.x + vec.y*vec.y + vec.z*vec.z)
    else:
        raise ValueError('please input a vector!')


def norm_2(vec) -> float:  # 计算模长的平方
    '''
    the absolute length of vector
    '''
    if isinstance(vec, GeVec2d):
        return vec.x*vec.x + vec.y*vec.y
    elif isinstance(vec, GeVec3d):
        return vec.x*vec.x + vec.y*vec.y + vec.z*vec.z
    else:
        raise ValueError('please input a vector!')


def unitize(vec) -> GeVec3d:  # 计算单位矢量
    '''
    convert a vector to be a unit vector
    '''
    if norm(vec) < PL_C:
        return vec  # raise ValueError('zero-vector has no unit vector!')
    if isinstance(vec, (GeVec2d, GeVec3d)):
        return (1.0 / norm(vec))*vec
    else:
        raise ValueError('please input a vector!')


def linspace(a, b, n) -> list:  # 产生线性分布
    if isinstance(a, GeVec2d) and isinstance(b, GeVec2d):
        return [GeVec2d(x, y) for (x, y) in zip(linspace(a.x, b.x, n), linspace(a.y, b.y, n))]
    elif isinstance(a, GeVec3d) and isinstance(b, GeVec3d):
        return [GeVec3d(x, y, z) for (x, y, z) in zip(linspace(a.x, b.x, n), linspace(a.y, b.y, n), linspace(a.z, b.z, n))]
    elif (isinstance(a, (int, float))) and (isinstance(b, (int, float))):
        d = a if(n == 1) else (b-a)/(n-1)
        return list(map(lambda x: a+x*d, range(n)))
    else:
        raise TypeError('linspace improper parameter!')


def dot(a: GeVec3d, b: GeVec3d) -> float:  # 矢量点积
    '''
    two vectors dot product
    '''
    if isinstance(a, GeVec2d) and isinstance(b, GeVec2d):
        return a.x*b.x + a.y*b.y  # quodratic sum, positive
    elif isinstance(a, GeVec3d) and isinstance(b, GeVec3d):
        return a.x*b.x + a.y*b.y + a.z*b.z
    elif is_all_vec([a, b]):
        return dot(to_vec3(a), to_vec3(b))  # vec compat
    else:
        raise TypeError('dot improper parameter!')


def cross(a: GeVec3d, b: GeVec3d) -> GeVec3d:  # 矢量叉积
    '''
    two vectors cross product
    '''
    if isinstance(a, GeVec2d) and isinstance(b, GeVec2d):
        return GeVec3d(0, 0, a.x*b.y-a.y*b.x)
    elif isinstance(a, GeVec3d) and isinstance(b, GeVec3d):
        return GeVec3d(a.y*b.z-a.z*b.y, a.z*b.x-a.x*b.z, a.x*b.y-a.y*b.x)
    elif is_all_vec([a, b]):
        return cross(to_vec3(a), to_vec3(b))  # vec compat
    else:
        raise TypeError('cross improper parameter!')

# ------------------------------------------------------------------------------------------
# |                                        TRANSFER                                        |
# ------------------------------------------------------------------------------------------


def to_vec2(*args):  # Vec3强转Vec2，删除z值
    # list transfer list, GeVec3d transfer GeVec2d
    if len(args) == 0:
        return []  # raise ValueError('parameter cannot be empty!')
    elif len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    elif len(args) == 1 and isinstance(args[0], GeVec2d):
        return args[0]
    elif len(args) == 1 and isinstance(args[0], GeVec3d):
        return GeVec2d(args[0].x, args[0].y)
    else:
        args = list(args)
        if not is_all_vec(args):
            raise ValueError('to_vec2 parameter type error!')
    for i in range(len(args)):
        if isinstance(args[i], GeVec3d):
            args[i] = GeVec2d(args[i].x, args[i].y)  # or using recursion
    return args


def to_vec3(*args):  # Vec2强转Vec3，z值置零
    # list return list, GeVec2d return GeVec3d
    if len(args) == 0:
        return []  # raise ValueError('parameter cannot be empty!')
    elif len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    elif len(args) == 1 and isinstance(args[0], GeVec3d):
        return args[0]
    elif len(args) == 1 and isinstance(args[0], GeVec2d):
        return GeVec3d(args[0].x, args[0].y, 0)
    elif len(args) == 2 and isinstance(args[0], GeVec2d) and isinstance(args[1], GeTransform):
        return args[1]*GeVec3d(args[0].x, args[0].y, 0)
    elif len(args) == 2 and isinstance(args[0], GeVec3d) and isinstance(args[1], GeTransform):
        return args[1]*args[0]
    elif len(args) == 2 and isinstance(args[0], (list, tuple)) and is_all_vec(args[0]) and isinstance(args[1], GeTransform):
        vecList = []  # create new list
        for iter in args[0]:
            vecList.append(args[1]*iter)
        return vecList
    else:
        args = list(args)
        if not is_all_vec(args):
            raise ValueError('to_vec3 parameter type error!')
    for i in range(len(args)):
        if isinstance(args[i], GeVec2d):
            args[i] = GeVec3d(args[i].x, args[i].y, 0)
    return args

# ------------------------------------------------------------------------------------------
# |                                       CALCULATE                                        |
# ------------------------------------------------------------------------------------------


# 求两个矢量之间的夹角，vectorA->vectorB右手定则，夹角为正
def get_angle_of_two_vectors(vectorA: GeVec3d, vectorB: GeVec3d, isAbs=False) -> float:
    # the angle range (turn left:0->pi / turn right:-pi->0)  # acos range [0, pi]
    if (norm(vectorA) * norm(vectorB) < PL_A):  # zero vector parallel/vertical to any
        return 0.0
    theta = math_acos(dot(vectorA, vectorB)/(norm(vectorA) * norm(vectorB)))
    if isAbs:
        return theta
    if cross(vectorA, vectorB).z < 0:  # the direction raletive to world-coord XoY
        theta = -theta
    return theta


def is_two_vectors_same_direction(vec1: GeVec3d, vec2: GeVec3d) -> str:  # 矢量同向判断
    '''
    DIRECTION_SAME  同向 
    DIRECTION_OPPO  反向 
    DIRECTION_VERTI  垂直 
    DIRECTION_NONE  无关 
    DIRECTION_ANY  任意（由于含零向量）
    '''
    if norm(vec1)*norm(vec2) < PL_A:
        # raise ValueError('please donot input zero vector!')
        return "DIRECTION_ANY"
    elif is_parallel(vec1, vec2):  # norm(cross(vec1, vec2)) < PL_A:  # parallel
        return "DIRECTION_SAME" if (dot(vec1, vec2) > 0) else "DIRECTION_OPPO"
    elif is_perpendi(vec1, vec2):  # abs(dot(vec1, vec2)) < PL_A:
        return "DIRECTION_VERTI"  # vertical
    else:
        return "DIRECTION_NONE"  # linearly independent


# is two vecotrs perpendicular (auto precision)
def is_perpendi(vecA: GeVec3d, vecB: GeVec3d) -> bool:
    if(is_float_zero(vecA.norm()) or is_float_zero(vecB.norm())):  # zero vector be any direction
        return True
    maxl = norm(vecA) if (norm(vecA) > norm(vecB)) else norm(vecB)
    return abs(dot(vecA, vecB)) < (maxl+1) * PL_E8


# is two vecotrs parallel (auto precision)
def is_parallel(vecA: GeVec3d, vecB: GeVec3d) -> bool:
    if(is_float_zero(vecA.norm()) or is_float_zero(vecB.norm())):  # zero vector be any direction
        return True
    maxl = norm(vecA) if (norm(vecA) > norm(vecB)) else norm(vecB)
    return norm(cross(vecA, vecB)) < (maxl+1) * PL_E8


# is two points coincident (auto precision)
def is_coincident(pointA: GeVec3d, pointB: GeVec3d) -> bool:
    maxl = norm(pointA) if (norm(pointA) > norm(pointB)) else norm(pointB)
    return norm(pointA - pointB) < (maxl+1) * PL_E8
