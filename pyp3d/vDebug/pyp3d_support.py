# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 功能函数
# Author: akingse
# Date: 2022/06

from .pyp3d_modeling import *

# ------------------------------------------------------------------------------------------
# |                                       COMBINE                                          |
# ------------------------------------------------------------------------------------------


def create_connect_middle_pipe(paramStart: list, paramEnd: list) -> Combine:  # 自动连接管接口
    '''
    startArc:Arc, ccw:bool=True, dExtend:float, length:float, scale:1.x=isLineBevel
    endArc:Arc,   cw:bool=False, dExtend:float, radius:float, scale:0=isArcBevel
    '''
    # startArc
    startArc = paramStart[0]
    centerS = get_matrixs_position(startArc.transformation)
    # using bool distinguish two direction
    vectorS = (2*float(paramStart[1])-1) * \
        get_matrixs_axisz(startArc.transformation)
    dExtendS = paramStart[2]
    # R1=get_scale_param(startArc.transformation).x
    pointS = centerS+dExtendS*unitize(vectorS)
    isLineS = bool(paramStart[4])

    # endArc
    endArc = paramEnd[0]
    centerE = get_matrixs_position(endArc.transformation)
    vectorE = (2*float(paramEnd[1])-1)*get_matrixs_axisz(endArc.transformation)
    dExtendE = paramEnd[2]
    # R2=get_scale_param(endArc.transformation).x
    pointE = centerE+dExtendE*unitize(vectorE)
    isLineE = bool(paramEnd[4])

    # points=[centerS,pointS,pointE,centerE]
    # show_points_line(points)
    # avR=(R1+R2)/2 #ensure radius equal
    # 半径保持一致，不一致时avR半径，规则需要设计

    geo = Combine()

    def _create_line_bevel(paramArc, pointsSec, withMiddle=False, end2=GeVec3d()):
        # pointsSec=[centerL,pointL,pointA]
        length = paramArc[3]
        lineEnd = pointsSec[1]+length * \
            unitize(pointsSec[2]-pointsSec[1])  # point
        pointsSec[2] = lineEnd  # change the bevel end point
        vectorP = (2*float(paramStart[1])-1) * \
            get_matrixs_axisz(paramArc[0].transformation)
        dExtendP = paramArc[2]
        sca = paramArc[4]
        secArc = Section(paramArc[0])
        secStart = trans((dExtendP-length)*unitize(vectorP))*secArc
        # using shadow method
        scaArc = Section(paramArc[0].transformation*scale(sca)
                         * inverse(paramArc[0].transformation)*paramArc[0])
        secMid = create_middle_shadow_section(
            scaArc, pointsSec, isMiddle=True)[0]
        secEnd = create_middle_shadow_section(
            secArc, pointsSec, isMiddle=False)[1]
        geoTemp = Combine()
        geoTemp.append(Loft([secArc, secStart]))
        geoTemp.append(Loft([secStart, secMid, secEnd]))
        if withMiddle:
            secEnd2 = trans(end2-lineEnd)*secEnd
            geoTemp.append(Loft(secEnd, secEnd2))
        return (geoTemp, lineEnd)  # extra return the next iterate point

    def _create_arc_bevel(paramArc, pointsSec, withMiddle=False, end2=GeVec3d()):
        # pointsSec=[centerA,pointA,pointL]
        secArc = Section(paramArc[0])
        axisZ = get_matrixs_axisz(get_matrix_from_three_points(pointsSec))
        arcBev = arc_of_segments_bevel(pointsSec, paramArc[3])
        arcStart = arcBev.pointStart  # arc start point
        arcEnd = arcBev.pointEnd  # arc end point
        arcCenter = arcBev.pointCenter  # arc center point
        # center of origin paramArc
        secStart = trans(arcStart-pointsSec[0])*secArc
        secEnd = arbitrary_rotate(arcCenter, axisZ, arcBev.scope)*secStart
        geoTemp = Combine()
        geoTemp.append(Loft([secArc, secStart]))
        geoTemp.append(Sweep(secStart, Line(arcBev)))
        if withMiddle:
            secEnd2 = trans(end2-arcEnd)*secEnd
            geoTemp.append(Loft([secEnd, secEnd2]))
        return (geoTemp, arcEnd)  # extra return the next iterate point

    if isLineS and isLineE:  # both isLineBevel
        pointsSec = [centerS, pointS, pointE]
        geoL1 = _create_line_bevel(paramStart, pointsSec, withMiddle=False)
        geo.append(geoL1[0])
        pointsSec = [centerE, pointE, pointS]
        geoL2 = _create_line_bevel(
            paramEnd, pointsSec, withMiddle=True, end2=geoL1[1])
        geo.append(geoL2[0])

    elif isLineS and (not isLineE):  # isLineBevel -> isArcBevel
        pointsSec = [centerS, pointS, pointE]
        geoL = _create_line_bevel(paramStart, pointsSec, withMiddle=False)
        geo.append(geoL[0])
        pointsSec = [centerE, pointE, pointS]
        geoA = _create_arc_bevel(
            paramEnd, pointsSec, withMiddle=True, end2=geoL[1])
        geo.append(geoA[0])

    elif (not isLineS) and isLineE:  # isArcBevel -> isLineBevel
        pointsSec = [centerE, pointE, pointS]
        geoL = _create_line_bevel(paramEnd, pointsSec, withMiddle=False)
        geo.append(geoL[0])
        pointsSec = [centerS, pointS, pointE]
        geoA = _create_arc_bevel(
            paramStart, pointsSec, withMiddle=True, end2=geoL[1])
        geo.append(geoA[0])

    else:  # both isArcBevel
        pointsSec = [centerS, pointS, pointE]
        geoA1 = _create_arc_bevel(paramStart, pointsSec, withMiddle=False)
        geo.append(geoA1[0])
        pointsSec = [centerE, pointE, pointS]
        geoA2 = _create_arc_bevel(
            paramEnd, pointsSec, withMiddle=True, end2=geoA1[1])
        geo.append(geoA2[0])

    return geo


# 获取临近点
def get_nearest_point_from_catch(catchList: list, mouse: GeVec3d, viewport=GeTransform(), num: int = 1) -> list:
    if len(catchList) == 0:
        return []
    axisZ = get_matrixs_axisz(viewport)
    # axisZ = get_matrixs_axisz(inverse_std(viewport))
    mat = shadow_vector_matrix_2D((-1.0)*axisZ)
    mouseSha = mat*mouse
    catchDict = {}  # map every catch-point and distance.
    for iter in catchList:
        catchDict[iter] = norm(mouseSha-mat*iter)
    # record all distance and sorted them.
    sortList = sorted(zip(catchDict.values(), catchDict.keys()))
    if num >= len(catchList):
        num = len(catchList)
    minList = []  # record the min distance.
    for i in range(num):
        minList.append(sortList[i][1])
    return minList


def get_terminal_port_from_catch(catchList: list, mouse: GeVec3d, viewport=GeTransform(), num: int = 1, angleMode=0) -> list:
    # [point]
    # [{point, R}]
    # [{point, vector}]
    # [{point, [R, vector]}]
    # [segment]
    # [{segment, R}]
    # [{segment, vector}]
    # [{segment, [R, vector]}]
    catchDict = {}
    # caution the relation of world-coord and viewport-coord
    axisz = get_matrixs_axisz(inverse_orth(viewport))
    # transform shadow pattern to viewport-coord, compare on viewport-coord.
    mat = viewport*shadow_vector_matrix_2D((-1.0)*axisz)
    mouseSha = mat * mouse
    for iter in catchList:
        d = norm(mouseSha - mat * iter[0])
        catchDict[iter] = d


# 在视图(投影)平面，获得到线段距离最近的点
def get_adsorb_point_on_line(line: Segment, mouse: GeVec3d, d: float, viewport: GeTransform) -> GeTransform:
    # 距离d触发捕捉，返回矩阵形式
    axisz = get_matrixs_axisz(inverse_orth(viewport))
    mat = viewport*shadow_vector_matrix_2D((-1.0)*axisz)
    mouseSha = mat * mouse
    lineR = mat*line
    if get_distance_of_point_line(mouseSha, lineR) <= d:
        point = get_nearest_point_of_point_line(mouseSha, lineR)
        return trans(viewport*point)
    else:
        return g_matrixE


# universal modeling to python parametrc component
def trans_um_to_ppc(sec: Section, line: list) -> Combine:
    vecZ = line[1]-line[0]
    # secZ=get_matrixs_axisz(sec.transformation) g_axisZ
    if is_parallel(vecZ, g_axisZ):
        secR = sec
    else:
        vecX = unitize(cross(g_axisZ, vecZ))
        vecY = unitize(cross(vecZ, vecX))
        mat = set_matrix_by_column_vectors(vecX, vecY, vecZ)
        secR = trans(line[0])*mat*sec
    return sweep_stere(secR, Line(line))
