# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 几何元素转换
# Author: akingse
# Date: 2022/01

from .pyp3d_component import *

# ------------------------------------------------------------------------------------------
# |                                        EXTRACT                                         |
# ------------------------------------------------------------------------------------------


# 从嵌套line中提取三维参数（矩阵作用后的绝对坐标，Vec2将转为Vec3）
def get_nested_parts_from_line(line: Line, keepSegment=False) -> list:
    mat = line.transformation
    partList = []
    for iter in line.parts:
        if isinstance(iter, (GeVec2d, GeVec3d)):
            partList.append(mat*to_vec3(iter))
        elif isinstance(iter, Segment):
            if keepSegment:
                partList.append(mat*iter)
            else:
                partList.append(mat*iter.start)
                partList.append(mat*iter.end)
        elif isinstance(iter, Arc):
            partList.append(mat*iter)
        elif isinstance(iter, SplineCurve):
            partList.append(mat*iter)
        elif isinstance(iter, Line):
            partChild = get_nested_parts_from_line(mat*iter)
            for iterC in partChild:
                partList.append(iterC)
        elif isinstance(iter, list):
            for iterP in iter:
                partList.append(mat*to_vec3(iterP))
        else:
            raise ValueError(
                'get_nested_parts_from_line parameter type error!')
    return partList


# 从section中提取三维参数
def get_nested_parts_from_section(sec: Section) -> list:
    # close willnot work, extract original parameter
    return get_nested_parts_from_line(sec.transformation*Line(sec.parts))


# 从Line获取分段轨迹线（返回三维参数）
def get_fragments_from_line(line: Line, close=False) -> list:
    parts = get_nested_parts_from_line(line)  # only vec3, no vec2
    lenL = len(parts)
    fragmList = []
    for i in range(lenL-1):  # only add fragment which norm greater than zero
        if isinstance(parts[i], (GeVec3d, Arc, SplineCurve, Segment)) and \
                isinstance(parts[i+1], (GeVec3d, Arc, SplineCurve, Segment)):
            if isinstance(parts[i], (Arc, SplineCurve, Segment)):
                fragmList.append(parts[i])
            if norm(get_part_end_point(parts[i])-get_part_start_point(parts[i+1])) > PL_A:
                fragmList.append(Segment(get_part_end_point(
                    parts[i]), get_part_start_point(parts[i+1])))
        else:
            raise ValueError('get_nested_parts_from_line parameter error!')
    _l = lenL-1
    if isinstance(parts[_l], (Arc, SplineCurve, Segment)):
        fragmList.append(parts[_l])
    # judge whether close
    if close:
        if isinstance(parts[_l], (GeVec3d, Arc, SplineCurve, Segment)) and \
                isinstance(parts[0], (GeVec3d, Arc, SplineCurve, Segment)):
            if norm(get_part_end_point(parts[_l])-get_part_start_point(parts[0])) > PL_A:
                fragmList.append(Segment(get_part_end_point(
                    parts[_l]), get_part_start_point(parts[0])))
        else:
            raise ValueError('get_nested_parts_from_line parameter error!')
    return fragmList


def get_fragments_from_section(sec: Section) -> list:
    return get_fragments_from_line(sec.transformation*Line(sec.parts), close=True)

# ------------------------------------------------------------------------------------------
# |                                         REFER                                          |
# ------------------------------------------------------------------------------------------


# 从line中提取出第一个参考点
def get_first_point_on_line(line: Line) -> GeVec3d:
    partList = get_nested_parts_from_line(line)
    if len(partList) == 0:
        raise ValueError('parameter number error!')
    return get_part_start_point(partList[0])


def get_first_point_on_section(sec: Section) -> GeVec3d:
    return get_first_point_on_line(sec.transformation*Line(sec.parts))


# 获取part的起点
def get_part_start_point(part) -> GeVec3d:
    if isinstance(part, (GeVec2d, GeVec3d)):
        return to_vec3(part)
    elif isinstance(part, Arc):
        return part.pointStart
    elif isinstance(part, Segment):
        return part.start
    elif isinstance(part, SplineCurve):
        return part.transformation*part.points[0]
    elif isinstance(part, Line) and len(part.parts) > 0:
        child = get_nested_parts_from_line(part)
        return get_part_start_point(child[0])
    elif isinstance(part, list) and len(part) > 0:
        if is_all_vec(part[0]):
            return part[0]
        else:
            return get_part_start_point(part[0])
    else:
        raise ValueError('parameter type error!')


# 获取part的终点
def get_part_end_point(part) -> GeVec3d:
    if isinstance(part, (GeVec2d, GeVec3d)):
        return to_vec3(part)
    elif isinstance(part, Arc):
        return part.pointEnd
    elif isinstance(part, Segment):
        return part.end
    elif isinstance(part, SplineCurve):
        return part.transformation*part.points[-1]
    elif isinstance(part, Line) and len(part.parts) > 0:
        child = get_nested_parts_from_line(part)
        return get_part_end_point(child[-1])
    elif isinstance(part, list) and len(part) > 0:
        if is_all_vec(part[-1]):
            return part[-1]
        else:
            return get_part_start_point(part[-1])
    else:
        raise ValueError('parameter type error!')
# get_start_point_of_line = get_part_start_point
# get_end_point_of_line = get_part_end_point


# 提取定位矩阵（相对坐标系位姿矩阵）
def get_first_matrix_from_line(line: Line) -> GeTransform:
    # cannot ensure line locate on unique plane
    parts = get_nested_parts_from_line(line)
    for iter in parts:  # using Arc first
        if isinstance(iter, Arc):
            return get_orthogonal_matrix(iter.transformation, True)
        elif isinstance(iter, SplineCurve):
            return get_orthogonal_matrix(iter.transformation)*get_matrix_from_points(iter.points)
    if is_all_vec(parts):
        return get_matrix_from_points(parts)
    else:  # GeTransform()
        raise ValueError('get_first_matrix_from_line param error!')


# 二维截面，transformation属性即三维矩阵
def get_matrix_from_section(sec: Section) -> GeTransform:
    return get_first_matrix_from_line(sec.transformation*Line(sec.parts))
    # return get_orthogonal_matrix(sec.transformation)


# ------------------------------------------------------------------------------------------
# |                                       SEGMENT                                          |
# ------------------------------------------------------------------------------------------


# 将point的list转换为segment的list
def get_segments_from_points(points: list, removeCoin=True, close=False) -> list:
    if removeCoin:
        points = remove_coincident_point(points)
    segmentList = []
    if len(points) == 0:
        return []
    for i in range(len(points)-1):
        segmentList.append(Segment(points[i], points[i+1]))
    if close:
        if norm(points[-1]-points[0]) > PL_A:
            segmentList.append(Segment(points[-1], points[0]))
    return segmentList


# 将segment的list转换为point的list
def get_points_from_segments(segments: list, removeCoin=True) -> list:
    lenP = len(segments)
    if lenP == 0:
        return []
    pointList = [segments[0].start]
    for iter in segments:
        pointList.append(iter.end)
    if removeCoin:
        pointList = remove_coincident_point(pointList)
    return pointList
