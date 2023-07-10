#################################################################
#                      1.0 兼容接口 预处理函数                    #
#################################################################
# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Author: akingse
# Date: 2021/08/07

from .pyp3d_relation import *


def to_section(*args) -> Section:  # 多点(>=3)生成一个二维Section面，已变换到3维
    '''
    many points (>=3) generate a section in 2-dimension, been translated to 3-dimension already
    '''
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        parts = list(args[0])
    else:
        parts = list(args)
    if is_all_vec2(parts):
        return Section(parts)
    forwM = get_first_matrix_from_line(Line(parts))
    if not is_parts_locate_on_plane(parts, forwM):  # judge whether same plane.
        raise ValueError('some part isnot on same plane!')
    invM = inverse(forwM)
    parts2D = []  # to two dimension
    for iter in parts:
        part = invM*iter
        parts2D.append(part)
    return forwM*Section(parts2D)


def get_matrix_from_contourline(contourLines):  # 从一个轮廓线中提取一个参考矩阵S
    # BPTransform getLocalMatrixFromCurveArray(GeCurveArrayPtr curveArray3)
    for iter in contourLines:
        if isinstance(iter, Arc):
            return get_orthogonal_matrix(iter.transformation)
    points = get_nested_parts_from_line(contourLines)  # contourLines nest line
    return get_matrix_from_points(points)


def get_plane_of_contourline(OuterContourparts) -> str:  # 判断所在坐标系平面
    # plane='XY' # default plane
    for part in OuterContourparts:
        if isinstance(part, Arc):
            vecotr0 = get_matrixs_axisx(part.transformation)
            vecotr90 = get_matrixs_axisy(part.transformation)
            vecotrV = cross(vecotr0, vecotr90)
            if norm(cross(vecotrV, g_axisX)) < PL_A:  # parallel
                return 'YZ'
            elif norm(cross(vecotrV, g_axisY)) < PL_A:
                return 'ZX'
            elif norm(cross(vecotrV, g_axisZ)) < PL_A:
                return 'XY'
            else:
                raise ValueError('cannot judge the locate plane!')
    points = []  # take out all point in Line()
    for part in OuterContourparts:
        if isinstance(part, Line):
            pointList = get_nested_parts_from_line(part)
            for iter in pointList:
                points.append(iter)
    pointA = points[0]
    sumX = sumY = sumZ = 0
    for pointI in points:
        sumX += abs((pointI-pointA).x)
        sumY += abs((pointI-pointA).y)
        sumZ += abs((pointI-pointA).z)
    if abs(sumX) < PL_A and abs(sumY) > PL_A and abs(sumZ) > PL_A:
        return 'YZ'
    elif abs(sumY) < PL_A and abs(sumX) > PL_A and abs(sumZ) > PL_A:
        return 'ZX'
    elif abs(sumZ) < PL_A and abs(sumX) > PL_A and abs(sumY) > PL_A:
        return 'XY'
    else:
        raise ValueError('cannot judge the locate plane!')


def polygon_to_ccw(points: list) -> list:  # 规范直线多边形,无自相交,无回头线,逆时针
    # ccw=counter clockwise
    if not is_all_num(points):
        return points
    points = to_vec2(points)  # force tobe Vec2
    points = remove_coincident_point(points)
    if len(points) < 3:
        raise ValueError(
            'please input 3 points at least, to compose one plane！')
    if is_polygon_self_intersect(points):
        raise ValueError('some lines self-intersect in polygon!')
    if judge_polygon_surface(points) < 0:
        points.reverse()
    return points


# 当RuledSweep中的两点重合，自动将第二个点（三维点）错开一个微小偏移
def set_points_offset(points: list) -> list:
    '''
    when two coincident in RuledSweep, auto offset the second point a tiny distance
    '''
    k = PL_A
    if norm(points[1]-points[0]) < PL_A:
        unitVec = unitize(points[0]-points[-1])
        points[1] = points[1]+k*unitVec
    for i in range(1, len(points)-1):
        if norm(points[i+1]-points[i]) < PL_A:
            unitVec = unitize(points[i]-points[i-1])
            points[i+1] = points[i+1]+k*unitVec
    return points


def rotation_to(v: GeVec3d) -> GeTransform:  # 旋转至与V同向
    '''
    rotate to the same direction as V
    '''
    transformation = GeTransform()  # transformation assign identity matrix
    v12_norm = norm(v)
    if v12_norm != 0.0:
        angle_z = acos(v.z/v12_norm)
        # if angle_z == 0.0:
        if abs(angle_z) < PL_A:
            transformation *= rotate(GeVec3d(0, 1, 0),  -pi/2)
        # elif angle_z == pi:
        elif abs(abs(angle_z)-pi) < PL_A:
            transformation *= rotate(GeVec3d(0, 1, 0),  pi/2)
        else:
            r_xy = sqrt(v.x**2 + v.y**2)
            angle_xy = acos(v.x/r_xy)
            if v.y < 0.0:
                angle_xy = -angle_xy
            transformation *= rotate(GeVec3d(0, 0, 1),  angle_xy) * \
                rotate(GeVec3d(0, 1, 0),  angle_z-pi/2)
    return transformation


def lean_section(pointY, pointX, theta=0) -> GeTransform:
    return rotz(atan2(pointY.y-pointX.y, pointY.x-pointX.x)+theta)


def get_angle_of_two_segments(segmA: Segment, segmB: Segment) -> float:
    return get_angle_of_two_vectors(segmA[1]-segmA[0], segmB[1]-segmB[0])


def sweep_straight(section: Section, line: Line) -> Loft:  # 平面直线扫掠函数
    section = roty(-pi/2)*section
    points = get_nested_parts_from_line(line)  # line.parts
    points = remove_coincident_point(points)
    if len(points) < 2:
        return
    lengP = len(points)
    lineList = []  # segment
    for i in range(lengP-1):
        lineList.append([points[i], points[i+1]])
    sectionList = [
        trans(points[0])*lean_section(points[1], points[0], 0)*section]
    for i in range(1, lengP-1):
        theta = get_angle_of_two_segments(lineList[i-1], lineList[i])/2
        shadM = scale(1/cos(theta), 1/cos(theta), 1)
        sectionI = trans(points[i])*shadM * \
            lean_section(points[i], points[i-1], theta)*section
        sectionList.append(sectionI)
    sectionList.append(
        trans(points[lengP-1])*lean_section(points[lengP-1], points[lengP-2], 0)*section)
    curveloft = Loft(sectionList)
    curveloft.smooth = True
    return curveloft


# ------------------------------------------------------------------------------------------
# |                                       BYNAME                                           |
# ------------------------------------------------------------------------------------------


BPParametricComponent = UnifiedModule(PARACMPT_PARAMETRIC_COMPONENT)
points_to_matrix = get_matrix_from_two_points
vector_to_matrix = get_matrix_from_one_vector
points_to_offset = set_points_offset
judge_polygon_surface = get_surface_of_polygon
points_to_segments = get_segments_from_points
is_point_locate_on_plane = is_point_on_plane
is_vertical = is_perpendi
straight_sweep = sweep_straight

# pyp3d_component
combine = Combine
GeLineString = Line
LineString = Line
PointString = Point
GePoint=Point
# pyp3d_matrix
rotation = rotate
translate = trans
translation = trans
reflect = mirror
inverse_std = inverse_orth
arbitrary_rotate = rotate_arbitrary
scale_shadow_matrix = shadow_scale_matrix
vector_shadow_matrix = shadow_vector_matrix_2D
