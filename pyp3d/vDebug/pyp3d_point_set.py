# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 点集处理函数
# Author: akingse
# Date: 2022/03
from .pyp3d_matrix import *


# ------------------------------------------------------------------------------------------
# |                                         MATRIX                                         |
# ------------------------------------------------------------------------------------------


# 两个点生成矩阵,可以交换axisX和axisZ
def get_matrix_from_two_points(point0: GeVec3d, point1: GeVec3d, isAxisZ=True) -> GeTransform:
    if norm(point1-point0) < PL_A:
        return trans(point0)
    axisZ = unitize(point1-point0)
    if (abs(axisZ.x) + abs(axisZ.y) < PL_A):  # axisZ g_axisZ parallel
        axisX = g_axisX
    elif (abs(axisZ.z) < PL_A):  # axisZ locate on XoY plane
        # (abs(axisZ.x) + abs(axisZ.z) < PL_A) or (abs(axisZ.y) + abs(axisZ.z) < PL_A)
        axisX = g_axisZ
    else:
        axisX = GeVec3d(axisZ.x, axisZ.y)
    axisY = unitize(cross(axisZ, axisX))
    axisX = unitize(cross(axisY, axisZ))
    if not isAxisZ:
        temp = axisZ
        axisZ = axisX
        axisX = temp
        axisY = (-1.0)*axisY
    return set_matrix_by_column_vectors(axisX, axisY, axisZ, point0)


def get_matrix_from_one_vector(vector: GeVec3d, isAxisZ=True) -> GeTransform:  # 一个列矢量创建矩阵
    return get_matrix_from_two_points(g_axisO, vector, isAxisZ)


def set_matrix_by_two_vectors(vecX: GeVec3d, vecY: GeVec3d, isOrth=True) -> GeTransform:  # 两个列矢量创建矩阵
    if norm(vecX)+norm(vecY) < PL_A:  # is all zero-vector
        return GeTransform()
    if (norm(vecX) * norm(vecY) < PL_A or norm(cross(vecX, vecY)) < PL_A):  # there is zero-vector or collinear
        return get_matrix_from_one_vector(vecX + vecY, False)
    if (isOrth):  # unit orthonormal
        vectorX = unitize(vecX)
        vectorZ = unitize(cross(vecX, vecY))
        vectorY = unitize(cross(vectorZ, vectorX))
        return set_matrix_by_column_vectors(to_vec3(vectorX), vectorY, vectorZ)
    else:
        vecZ = unitize(cross(vecX, vecY))
        return set_matrix_by_column_vectors(vecX, vecY, vecZ)


# 通过两个矢量创建矩阵（单位正交姿态矩阵）
def get_matrix_from_two_vectors(vec1: GeVec3d, vec2: GeVec3d, isOrth=True) -> GeTransform:
    return set_matrix_by_two_vectors(vec1, vec2, isOrth)


# 用且仅用3个点生成位姿矩阵
def get_matrix_from_three_points(points: list, is2D=True) -> GeTransform:
    # point1 is position, point2-point1 is axisX, vec1×vec2 is axisZ
    # if len(points)<3:
    #     raise ValueError('parameter amount error!')
    if len(points) == 0:
        return GeTransform()
    elif len(points) == 1:
        return GeTransform() if is2D else trans(points[0])
    elif len(points) == 2:
        return get_matrix_from_two_points(points[0], points[1])
    else:
        vecA = points[1]-points[0]
        vecB = points[2]-points[1]
        forwM = trans(points[0])*set_matrix_by_two_vectors(vecA, vecB)
        return GeTransform() if (is_two_dimensional_matrix(forwM) and is2D) else forwM


def get_matrix_from_points(points: list, is2D=True) -> GeTransform:  # 用多个点生成矩阵
    # auto skip coincident point and collinear point, if cannot judge location return g_matrixE
    if len(points) == 0:
        return GeTransform()
    points = to_vec3(points)
    vecA = GeVec3d()
    vecB = GeVec3d()
    indexA = 0
    for i in range(1, len(points)):
        if norm(points[i]-points[0]) > PL_A:  # pointO
            vecA = points[i]-points[0]
            indexA = i
            break
    for j in range(indexA+1, len(points)):
        if norm(points[j]-points[indexA]) > PL_A and norm(cross(vecA, points[j]-points[indexA])) > PL_A:  # pointA
            vecB = points[j]-points[indexA]
            break
    rotM = set_matrix_by_two_vectors(vecA, vecB)
    forwM = trans(points[0])*rotM
    # if is2D=True, two_dimensional will return unit g_matrixE.
    return GeTransform() if (is_two_dimensional_matrix(forwM) and is2D) else forwM


def get_arc_from_three_points(args: list) -> tuple:  # 用且仅用3个点生成圆弧（矩阵和圆弧角）
    args = copy.deepcopy(args)
    if len(args) != 3:
        raise TypeError("get_arc_from_three_points number error!")
    args = to_vec3(args)
    forwM = get_matrix_from_three_points(args, True)
    invM = inverse_orth(forwM)
    point1 = invM*(args[0])  # points cannot collinear
    point2 = invM*(args[1])
    point3 = invM*(args[2])
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x3, y3 = point3.x, point3.y
    yc = ((x3-x2)*(x3**2+y3**2-x1**2-y1**2)-(x3-x1)*(x3**2+y3 **
          2-x2**2-y2**2)) / (2*(x3-x2)*(y3-y1)-2*(x3-x1)*(y3-y2))
    xc = ((y3-y2)*(x3**2+y3**2-x1**2-y1**2)-(y3-y1)*(x3**2+y3 **
          2-x2**2-y2**2)) / (2*(y3-y2)*(x3-x1)-2*(y3-y1)*(x3-x2))
    pointC = GeVec3d(xc, yc)
    R = sqrt((xc-x1)**2+(yc-y1)**2)
    arcMat = forwM*trans(xc, yc)*scale(R)*rotz(atan2(y1-yc, x1-xc))
    agInter = get_angle_of_two_vectors(point1-pointC, point3-pointC, False)
    agCircu = get_angle_of_two_vectors(point1-point2, point3-point2, False)
    if agInter < 0 and agCircu < 0:  # using intersect angle judge direciton
        scope = agInter+2*pi
    elif agInter > 0 and agCircu > 0:
        scope = agInter-2*pi
    else:
        scope = agInter
    return (arcMat, scope)


def mirror_point_of_line(point: GeVec3d, line: list) -> GeVec3d:  # 点关于线镜像
    mat = get_matrix_from_three_points([line[0], line[1], point], False)
    return mirror(mat, "XoZ")*point


def shadow_vector_matrix_3D(vec: GeVec3d) -> GeTransform:  # 三维投影矩阵
    # the two dimensional foil matrix.
    mat = GeTransform([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
    rela = get_matrix_from_one_vector(vec, True)
    return rela*mat*inverse(rela)

# ------------------------------------------------------------------------------------------
# |                                        RELATION                                        |
# ------------------------------------------------------------------------------------------


def is_points_collinear(points: list) -> bool:  # 判断不重合的点是否共线
    # 全部共线，return True
    points = remove_coincident_point(points)
    if len(points) < 3:
        return True  # raise ValueError('please input more than 3 points!')
    vectorA = points[1]-points[0]
    normA = norm(vectorA)
    for i in range(2, len(points)):
        vectorI = points[i]-points[0]
        if abs(abs(dot(vectorA, vectorI))-normA*norm(vectorI)) > PL_A:
            return False
    return True


def is_points_on_same_plane(points: list) -> bool:  # 判断多点是否在同一个平面上
    if is_all_vec2(points):
        return True
    points3D = to_vec3(points)
    vectorZ = get_matrixs_axisz(get_matrix_from_points(points3D))
    for iter in points3D:  # using range to exclude front 3 points
        if abs(dot(iter-points3D[0], vectorZ)) > PL_A:
            return False
    return True


def remove_coincident_point(points: list, isAll=False) -> list:
    if len(points) == 0:
        return points
    solePoints = [points[0]]  # lonePoints
    if isAll:  # traversal all points, remove all coincident
        for i in range(1, len(points)):
            isLone = True
            for p in solePoints:
                if norm(points[i]-p) < PL_E8:
                    isLone = False
                    break
            if isLone:
                solePoints.append(points[i])
        return solePoints
    else:  # only remove adjacent coincident
        j = 0
        for i in range(1, len(points)):
            if norm(points[i]-solePoints[j]) > PL_E8:
                solePoints.append(points[i])
                j = j+1
        return solePoints


def remove_collinear_point(pointsO: list) -> list:  # 三维共线点去重
    points = remove_coincident_point(pointsO)
    if len(points) <= 2:
        return points
    soloPoints = [points[0], points[1]]  # foldPoints
    for i in range(2, len(points)):
        vectorF = soloPoints[-1]-soloPoints[-2]  # the front vector
        vectorL = points[i]-soloPoints[-1]  # the current vector
        if abs(abs(dot(vectorF, vectorL))-norm(vectorF)*norm(vectorL)) < PL_A:  # collinear
            soloPoints.pop()  # pop(-1)
        soloPoints.append(points[i])
        # to ensure valid local matrix, same direction points, update current point,
        # oppo direction points, pop off the prior point.
    return soloPoints


# 纯多边形强制统一平面
def get_points_on_unified_plane(points) -> list:
    # get a locate plane, another point will delete z value, force to put same plane.
    forwM = get_matrix_from_points(points)  # get refer matrix
    invM = inverse_orth(forwM)
    pointUnity = []
    for iter in points:
        pointI = to_vec2(invM*iter)
        pointUnity.append(forwM*to_vec3(pointI))
    return pointUnity


# 两点线段设置微小偏移量
def get_much_offset_points_from_two_points(segment: list, num: int, isStart=True) -> list:
    # last two to last one, the points set of last point.
    k = PL_A
    pointStart = segment[0]  # list type of segment
    pointEnd = segment[1]
    pointList = []
    unitVec = unitize(pointEnd-pointStart)
    if isStart:
        for i in range(num):
            pointList.append(i*k*unitVec+pointStart)
    else:
        for i in range(num):
            pointList.append(pointEnd-(num-1-i)*k*unitVec)
    return pointList


# 判断点是否在平面上（矩阵XOY面）
def is_point_on_plane(point: GeVec3d, plane: GeTransform) -> bool:
    pointO = get_matrixs_position(plane)  # the original point
    vectorZ = get_matrixs_axisz(get_orthogonal_matrix(plane))
    return is_perpendi(vectorZ, point - pointO)
    # return abs(dot(vectorZ, point - pointO)) < PL_E8


# 获取点到平面的距离（矩阵XOY面）
def get_distance_of_point_plane(point: GeVec3d, plane: GeTransform, isAbs=True) -> float:
    pointRela = inverse_orth(get_orthogonal_matrix(plane))*point
    # relative value, with sign
    return abs(pointRela.z) if isAbs else pointRela.z


# 三点平面生成镜像矩阵
def mirror_of_plane(*args: list) -> GeTransform:
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    else:
        args = list(args)
    return mirror(get_matrix_from_three_points(args), "xoy")


# 提取嵌套列表
def get_nested_parts_from_list(parts: list) -> list:
    if not isinstance(parts, (list, tuple)):
        return parts
    partsList = []
    for iter in parts:
        if isinstance(iter, (list, tuple)):
            partsList += get_nested_parts_from_list(iter)
        else:
            partsList.append(iter)
    return partsList


# ------------------------------------------------------------------------------------------
# |                                        POLYGON                                         |
# ------------------------------------------------------------------------------------------


def get_surface_of_triangle(trigon: list) -> float:  # 三角形面积
    if len(trigon) < 3:
        return 0.0
    a = norm(trigon[1]-trigon[0])
    b = norm(trigon[2]-trigon[0])
    c = norm(trigon[2]-trigon[1])
    return sqrt((a+b+c)*(-a+b+c)*(a-b+c)*(a+b-c))/4


def is_point_in_triangle(point: GeVec3d, trigon: list) -> bool:  # 点是否在三角形内
    if len(trigon) != 3:
        return False
    # surface equal
    sS = get_surface_of_triangle(trigon)
    s1 = get_surface_of_triangle([point, trigon[0], trigon[1]])
    s2 = get_surface_of_triangle([point, trigon[1], trigon[2]])
    s3 = get_surface_of_triangle([point, trigon[2], trigon[0]])
    # return abs(sS-s1-s2-s3) < PL_A
    # vector cross product
    pA = trigon[0]
    pB = trigon[1]
    pC = trigon[2]
    # judge whether point between included angle
    betA = is_two_vectors_same_direction(
        cross(pB-pA, point-pA), cross(pC-pA, point-pA))
    betB = is_two_vectors_same_direction(
        cross(pA-pB, point-pB), cross(pC-pB, point-pB))
    # points locate on same side.
    sdA = cross(point-pA, pB-pA)
    sdB = cross(point-pB, pC-pB)
    sdC = cross(point-pC, pA-pC)
    # same direction
    return abs(norm(sdA)*norm(sdB)-dot(sdA, sdB)) < PL_A and abs(norm(sdA)*norm(sdC)-dot(sdA, sdC)) < PL_A


def get_surface_of_polygon(points: list) -> float:  # 通过面积判断二维多边形方向
    '''
    return the truly surface area, anti-clockwise, surface>0
    '''
    lenP = len(points)
    if lenP < 3:
        return 0.0
    Surfacex2 = 0.0
    for i in range(lenP-1):
        Surfacex2 += points[i].x * points[i+1].y-points[i+1].x*points[i].y
    Surfacex2 += points[lenP-1].x * points[0].y-points[0].x * points[lenP-1].y
    return Surfacex2/2


def get_range_of_polygon(polygon: list) -> list:  # polygon surrounded box
    if len(polygon) == 0:
        return [0, 0, 0, 0, 0, 0]
    xMin = xMax = polygon[0].x
    yMin = yMax = polygon[0].y
    zMin = zMax = polygon[0].z
    for i in polygon:
        if i.x > xMax:
            xMax = i.x
        if i.x < xMin:
            xMin = i.x
        if i.y > yMax:
            yMax = i.y
        if i.y < yMin:
            yMin = i.y
        if i.z > zMax:
            zMax = i.z
        if i.z < zMin:
            zMin = i.z
    return (xMin, xMax, yMin, yMax, zMin, zMax)
