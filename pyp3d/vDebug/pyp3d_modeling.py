# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 新的造型函数
# Author: fishmeng akingse
# Date: 2021/12

from .pyp3d_api import *
from .pyp3d_function import *

# ------------------------------------------------------------------------------------------
# |                                         SWEEP                                          |
# ------------------------------------------------------------------------------------------


# section截面位置方向不变，line为相对路径
def sweep_stere(sec: Section, line: Line, isSmooth=False) -> Combine:
    '''new linear sweep in 3-dimension'''
    points = get_nested_parts_from_line(line)
    if not is_all_vec(points):  # parameter check
        raise ValueError('sweep_stere only support points!')
    segms = get_segments_from_points(points)
    lenSegm = len(segms)
    # lenPoint=len(points)
    if lenSegm == 1:
        return Sweep(sec, line)
    # is line start point locate on first section
    if not is_point_in_contourline(points[0], sec):
        # get the refer point, to decide relative sweep path.
        pointRefer = get_first_point_on_section(sec)-points[0]
    else:
        pointRefer = g_axisO  # referM=GeTransform()
    secRefer = trans((-1.0)*pointRefer)*sec
    if lenSegm == 2:
        secMid, secLast = create_middle_shadow_section(
            secRefer, points, False)
        secList = [secRefer, secMid, secLast]
        geo = Loft(secList)
    else:  # lenSegm>=3
        # while close or open path.
        secList = create_middle_discrete_sections(
            secRefer, points, is_coincident(points[0], points[len(points)-1]))
        # for i in range(lenSegm):
        #     secI = Section(get_discrete_points_from_section(secList[i], 30))
        #     secII = Section(get_discrete_points_from_section(secList[i+1], 30))
        #     if is_two_sections_intersect(secI, secII) == "NOT_COPLANAR_INTER":
        #         raise ValueError('some section self-intersect!')
        geo = Loft(secList)
        geo.smooth = isSmooth
    return trans(pointRefer)*geo


# 与轨迹线等距平行的sweep
def sweep_parallel(sec: Section, line: Line) -> Combine:
    polyline = get_nested_parts_from_line(line)
    if not is_all_vec3(polyline) or len(polyline) < 3:
        raise TypeError("")
    pStart = get_first_point_on_section(sec)
    paraList = [pStart]
    # using 3D
    d = get_distance_of_point_line(pStart, Segment(polyline[0], polyline[1]))
    # d = norm(A-P+dot(A-B, A-P)/dot(B-A, B-A)*(B-A))
    for i in range(len(polyline)-2):
        A = polyline[i]
        B = polyline[i+1]
        C = polyline[i+2]
        P = paraList[-1]  # len(points)-1
        # angle = get_angle_of_two_vectors(B-A, C-B)
        mat = get_matrix_from_three_points([A, B, C], False)
        if (inverse_std(mat)*P).y >= 0:  # in angle
            sign = -1.0
        else:
            sign = 1.0
        m = (A-B)+dot((C-B), (B-A))/dot((C-B), (C-B))*(C-B)
        n = (B-P)-dot((C-B), (B-P))/dot((C-B), (C-B))*(C-B)
        k = 0
        if not is_float_zero(dot(m, m)):
            k = (-2*dot(m, n)+sign*sqrt(4*dot(m, n)*dot(m, n)-4 *
                                        dot(m, m)*(dot(n, n)-d * d)))/(2*dot(m, m))
        if k < 0:
            raise TypeError("")
        pIter = P+k*(B-A)
        paraList.append(pIter)
    matS = get_matrix_from_three_points(
        [polyline[0], polyline[1], pStart], False)
    matE = get_matrix_from_three_points(
        [polyline[-1], 2*polyline[-1]-polyline[-2], paraList[-1]], False)
    pLast = (matE*inverse_std(matS))*pStart
    paraList.append(pLast)
    geo = sweep_stere(sec, Line(paraList))
    return geo


# 获取直线扫掠截面列表
def create_middle_discrete_sections(sec: Section, points: list, isClose=False) -> list:
    # middle function, all preconditions are met. point in polygon, open path.
    segms = get_segments_from_points(points)
    if isClose:
        secIter = sec
        #first point and last point must coincident
        pointsTemp = [points[1], points[0], points[len(points)-2]]
        secFirst = create_middle_shadow_section(secIter, pointsTemp, True)[0]
        secList = [secFirst]
        for i in range(len(segms)-1):
            pointsTemp = [points[i], points[i+1], points[i+2]]
            secMid, secIter = create_middle_shadow_section(
                secIter, pointsTemp, True)
            secList.append(secMid)
        secList.append(secFirst)  # add first section
    else:
        secList = [sec]
        secIter = sec
        for i in range(len(segms)-1):
            pointsTemp = [points[i], points[i+1], points[i+2]]
            secMid, secIter = create_middle_shadow_section(
                secIter, pointsTemp, True)
            secList.append(secMid)
        secLast = trans(points[len(points)-1]-points[len(points)-2])*secIter
        secList.append(secLast)
    return secList


# 生成中间截面（投影+迭代）
def create_middle_shadow_section(secInput, pointsIter, isMiddle=True) -> list:
    # isMiddle control the secIter is middle corner-section or last-section.
    forwM = get_matrix_from_three_points(pointsIter, False)
    invM = inverse_orth(forwM)
    # because of relative axixZ rotate, rotz attached direction.
    intAngle = abs(get_angle_of_two_vectors(
        pointsIter[1]-pointsIter[0], pointsIter[2]-pointsIter[1]))
    # on the relative coordinate system.
    secRela = invM*secInput
    pointsRela = invM*pointsIter
    # the middle shadow section, perpendicular to trajctory, eqaully divided by angle.
    secShadowO = shadow_vector_matrix_2D(g_axisX)*secRela
    # on relative coordinate, axisX is first vector.
    pointShadow = get_nearest_point_of_point_line(
        g_axisO, Segment(pointsRela[0], pointsRela[1]))
    secShadow = trans(pointsRela[0]-pointShadow)*secShadowO
    shaMat = trans(pointsRela[1]-pointsRela[0])*shadow_scale_matrix(intAngle/2)
    secMag = forwM*shaMat*secShadow  # the shadow enlarge seciton.
    # sec iterate to next.
    if isMiddle:  # rotate and translate, to create next section.
        secIter = forwM*trans(pointsRela[1] -
                              pointsRela[0])*rotz(intAngle)*secRela
    else:  # the next section position.
        secIter = forwM*trans(pointsRela[2] -
                              pointsRela[0])*rotz(intAngle)*secRela
    return (secMag, secIter)


# 离散曲线sweep(单一截面)
def sweep_curve_discrete(sec: Section, line: Line) -> Combine:
    if is_all_vec(line.parts):
        return sweep_stere(sec, line)
    fragms = get_fragments_from_line(line, False)
    lenFrag = len(fragms)
    if lenFrag == 1:
        return Sweep(sec, line)
    # sweep_line_arc_stere
    geo = Combine()
    pointFirst = get_first_point_on_line(line)
    if not is_point_in_contourline(pointFirst, sec):
        pointRefer = get_first_point_on_section(sec)-pointFirst
    else:
        pointRefer = g_axisO
    secRefer = trans((-1.0)*pointRefer) * sec
    disNum = 0
    disRecord = []
    disFragm = []
    pointsDis = []
    for iter in fragms:
        if isinstance(iter, Segment):
            disRecord.append(disNum)
            disNum += 1
            disFragm.append(1)
            pointsDis.append(iter.start)
        elif isinstance(iter, Arc):
            disNumA = int(degrees(abs(iter.scope))/5)
            disFragm.append(disNumA)
            disRecord.append(disNum)
            disNum += disNumA
            pointsA = get_discrete_points_from_arc(iter, disNumA, False, True)
            pointsDis += pointsA
        # elif isinstance(iter, SplineCurve):
    disNum += 1  # the last point
    pointsDis.append(get_part_end_point(fragms[-1])) # the -1 index only in python
    # correct the first section
    if isinstance(fragms[0], (Arc, SplineCurve)):  # need correct
        secFirst = secRefer
        secRefer = rotate_arbitrary(pointsDis[0], fragms[0].vectorNormalC,
                                    get_angle_of_two_vectors(fragms[0].vectorTangentS, pointsDis[1]-pointsDis[0], False))*secRefer
    # elif isinstance(fragms[0], SplineCurve):
    #     secFirst = secRefer
    #     pointsCtrl = fragms[0].get_points()
    #     angle = get_angle_of_two_vectors(
    #         pointsCtrl[1]-pointsCtrl[0], pointsDis[1]-pointsDis[0], False)
    #     secRefer = rotate_arbitrary(pointsCtrl[0], get_matrixs_axisz(
    #         get_matrix_from_points(pointsCtrl)), angle)*secRefer
    isClose = is_line_close(line)
    secList = create_middle_discrete_sections(
        secRefer, pointsDis, isClose)
    for i in range(len(fragms)):
        if isinstance(fragms[i], Segment):
            loftI = Loft(secList[disRecord[i]], secList[disRecord[i]+1])
            geo.append(loftI)
        elif isinstance(fragms[i], Arc):
            secArc = []
            secCornerS = Section(get_discrete_points_from_section(
                secList[disRecord[i]], 30))
            secCornerE = Section(get_discrete_points_from_section(
                secList[disRecord[i] + disFragm[i]], 30))
            for j in range(disFragm[i]+1):
                secIterDis = Section(get_discrete_points_from_section(
                    secList[disRecord[i]+j], 30))  # discrete to judge intersect
                if is_two_sections_intersect(secIterDis, secCornerS) != "NOT_COPLANAR_INTER" and \
                        is_two_sections_intersect(secIterDis, secCornerE) != "NOT_COPLANAR_INTER":
                    secArc.append(secList[disRecord[i]+j])
            if i == 0 and (not isClose):  # here correct first seciton
                del secArc[0]
                secArc = [secFirst]+secArc
            if i == len(fragms)-1 and (not isClose):  # here correct last seciton
                secLast = secArc[-1]
                secLast = rotate_arbitrary(pointsDis[-1], fragms[-1].vectorNormalC,
                                           -get_angle_of_two_vectors(fragms[-1].vectorTangentE, pointsDis[-1]-pointsDis[-2], False))*secLast
                del secArc[-1]
                secArc.append(secLast)
            loftI = Loft(secArc)
            loftI.smooth = True
            geo.append(loftI)
    return trans(pointRefer)*geo


# 扫掠样条线
def sweep_spline(sec: Section, spline: SplineCurve) -> Loft:
    pointFirst = spline.get_points[0]
    if not is_point_in_contourline(pointFirst, sec):
        pointRefer = get_first_point_on_section(sec)-pointFirst
    else:
        pointRefer = g_axisO
    secRefer = trans((-1.0)*pointRefer) * sec
    disNum = 10*len(spline.points)
    points = get_discrete_points_from_spline(spline, disNum, True)
    secFirst = secRefer
    pointsCtrl = spline.get_points
    mat = get_matrix_from_points(pointsCtrl)
    angle = get_angle_of_two_vectors(
        pointsCtrl[1]-pointsCtrl[0], points[1]-points[0], True)
    secRefer = rotate_arbitrary(
        pointsCtrl[0], get_matrixs_axisz(mat), angle)*secRefer
    secListS = create_middle_discrete_sections(secRefer, points)
    secList = [secFirst]
    secStart = secListS[0]
    secEnd = secListS[-1]
    for i in range(1, disNum):
        if is_two_sections_intersect(secListS[i], secStart) != "NOT_COPLANAR_INTER" and \
                is_two_sections_intersect(secListS[i], secEnd) != "NOT_COPLANAR_INTER":
            secList.append(secListS[i])
    loft = Loft(secList)
    loft.smooth = True
    return loft


# 扫掠椭圆弧
def sweep_arc(sec: Section, line: Line) -> Loft:
    parts = get_nested_parts_from_line(line)
    if len(parts) != 1 or (not isinstance(parts[0], Arc)):
        raise TypeError('only sweep arc!')
    arc = parts[0]
    if arc.isCircle:
        return Sweep(sec, line)
    forwM = get_orthogonal_matrix(arc.transformation)
    arcR = inverse_orth(forwM)*arc  # relative arc
    secR = inverse_orth(forwM)*sec  # relative section
    disNum = int(degrees(abs(arc.scope))/5)
    if disNum < 5:
        disNum = 5
    pFirst = get_first_point_on_section(secR)
    aFirst = arcR.pointStart
    if is_point_in_contourline(aFirst, secR):
        arcScale = arcR
    else:  # the arc scale rule
        arcScale = scale(norm(pFirst)/norm(aFirst))*arcR
    # all discrete point list
    points = get_discrete_points_from_arc(arcScale, disNum, True, True)
    if arcScale.isFull:
        return forwM*sweep_stere(secR, Line(points), True)
    # arc start tangent vector angle, make correction.
    if not is_point_in_contourline(points[0], secR):
        pointRefer = get_first_point_on_section(secR)-points[0]
    else:
        pointRefer = g_axisO
    secRefer1 = trans((-1.0)*pointRefer)*secR
    secRefer = rotate_arbitrary(points[0], arcScale.vectorNormalC,
                                get_angle_of_two_vectors(arcScale.vectorTangentS, points[1]-points[0], False))*secRefer1
    secList = create_middle_discrete_sections(secRefer, points, False)
    secListArc = [secRefer1]
    secCornerS = Section(get_discrete_points_from_section(
        secList[0], 30))  # secList[0]
    secCornerE = Section(get_discrete_points_from_section(
        secList[-1], 30))  # secList[-1]
    for i in range(1, len(points)-1):  # avoid arc shadow
        secIter = Section(get_discrete_points_from_section(secList[i], 30))
        if is_two_sections_intersect(secIter, secCornerS) != "NOT_COPLANAR_INTER" and \
                is_two_sections_intersect(secIter, secCornerE) != "NOT_COPLANAR_INTER":
            secListArc.append(secList[i])
    secLast = rotate_arbitrary(points[-1], arcScale.vectorNormalC,
                               -get_angle_of_two_vectors(arcScale.vectorTangentE, points[-1]-points[-2], False))*secList[-1]
    secListArc.append(secLast)
    geo = Loft(secListArc)
    geo.smooth = True
    return forwM*trans(pointRefer)*geo


# ------------------------------------------------------------------------------------------
# |                                        FUSION                                          |
# ------------------------------------------------------------------------------------------


# 多个单一线条包围的sweep
def sweep_surround_lines(*args) -> Loft:
    # created by menghanyu
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    else:
        args = list(args)
    # parameters check
    if len(args) < 3:
        raise ValueError('parameter not enough!')
    fragms = []  # to compat Line
    for iter in args:
        if isinstance(iter, Line):
            fragments = get_fragments_from_line(iter)
            if len(fragments) != 1:
                raise ValueError('parameter type error!')
            iter = fragments[0]
            # iter = get_nested_parts_from_line(iter)[0]
        if not isinstance(iter, (Arc, SplineCurve, Segment)):
            raise ValueError('parameter type error!')
        fragms.append(iter)
    # judge whether coplanar
    pointStartL = []
    pointEndL = []
    # fragms discrete record
    discNum = 20
    lineList = []
    sweepSection = []
    for iter in fragms:
        pointStartL.append(get_part_start_point(iter))
        pointEndL.append(get_part_end_point(iter))
        points = get_discrete_points_from_fragment(iter, discNum, True)
        lineList.append(points)
    if not is_points_on_same_plane(pointStartL):
        raise ValueError('start points on different plane!')
    if not is_points_on_same_plane(pointEndL):
        raise ValueError('end points on different plane!')
    for i in range(discNum):
        sectionTemp = []
        for j in range(len(lineList)):
            sectionTemp.append(lineList[j][i])
        polygon_to_ccw(get_points_on_unified_plane(sectionTemp))
        sectionDisc = to_section(get_points_on_unified_plane(sectionTemp))
        sweepSection.append(sectionDisc)
    geo = Loft(sweepSection)
    geo.smooth = True
    return geo


# 绕原点向上的螺旋
def sweep_twist(sec: Section, height: float, pitch: float, isDiscrete=True, isCcw=True) -> Loft:
    if isDiscrete:
        pointList = get_discrete_points_from_section(sec, 0, True)
        secDis = to_section(pointList)
    else:
        secDis = sec
    secList = []
    discretNum = floor(height)//2 #integer divede
    sign = 2*float(isCcw)-1
    for i in range(discretNum+1):
        secList.append(trans(0, 0, height*i/discretNum) *
                       rotz(sign*height/pitch*2*pi*i/discretNum)*secDis)
    geo = Loft(secList)
    geo.smooth = True
    return geo


# 引导线控制缩放的Sweep，相对原点的缩放
def sweep_guide_line(sec: Section, lineX: SplineCurve, lineY: SplineCurve) -> Loft:
    if isinstance(lineX, SplineCurve) and isinstance(lineY, SplineCurve):
        pointsX = spline_curve_quasi(lineX.points, lineX.num, lineX.k)
        pointsY = spline_curve_quasi(lineY.points, lineY.num, lineY.k)
    elif isinstance(lineX, list) and isinstance(lineY, list):
        pointsX = lineX
        pointsY = lineY
    else:
        raise ValueError('parameter type error!')
    pointX = pointsX[0]
    pointY = pointsY[0]
    if not (is_point_on_contourline(pointX, sec) and is_point_on_contourline(pointY, sec)):
        raise ValueError('first point must on contourline!')
    if len(pointsX) != len(pointsY):
        raise ValueError('parameter number error!')
    disSecNum = len(pointsX)  # layer
    secList = []
    if abs(pointX.x) < PL_A:
        pointX = GeVec3d(1, pointX.y, pointX.z)
    if abs(pointY.y) < PL_A:
        pointsY = GeVec3d(pointX.x, 1, pointX.z)
    for i in range(disSecNum):
        mat = trans(0, 0, pointsX[i].z) * \
            scale(pointsX[i].x/pointX.x, pointsY[i].y/pointY.y)
        secList.append(mat*sec)
    geo = Loft(secList)
    geo.smooth = True
    return geo


# ------------------------------------------------------------------------------------------
# |                                         LOFT                                           |
# ------------------------------------------------------------------------------------------


# 轮廓边等比例放样
def loft_different_ratio(sec1: Section, sec2: Section) -> Loft:
    lengthB = get_perimeter_of_section(sec1)
    disNum = int(lengthB/20) if int(lengthB/20) >= 50 else 50
    distLayer = get_distance_of_point_plane(
        get_first_point_on_section(sec2), sec1.transformation)
    layerNum = int(distLayer/20) if int(distLayer/20) >= 10 else 10
    points1 = get_discrete_points_from_section(
        sec1, disNum, False)  # using for single section
    points2 = get_discrete_points_from_section(sec2, disNum, False)
    sectionList = []
    for i in range(layerNum+1):  # discrete layer
        pointsTemp = []
        for j in range(disNum):  # discrete contourline
            pointJ = points1[j]+(i/layerNum)*(points2[j]-points1[j])
            pointsTemp.append(pointJ)
        pointListU = get_points_on_unified_plane(pointsTemp)
        if is_polygon_self_intersect(pointListU):
            raise ValueError('some lines self-intersect in polygon!')
        sectionList.append(Section(pointListU))
    geo = Loft(sectionList)
    geo.smooth = True
    return geo


# loft异面放样融合算法
def loft_different(sec1: Section, sec2: Section) -> Loft:
    # created by menghanyu
    segm1 = get_fragments_from_section(sec1)
    segm2 = get_fragments_from_section(sec2)
    if (len(segm1) >= len(segm2)):  # discrete much contourline priority.
        segmB = segm1  # base section
        segmT = segm2  # top section
        secB = sec1
        secT = sec2
    else:
        segmB = segm2
        segmT = segm1
        secB = sec2
        secT = sec1
    if len(segmT) == 1:  #
        return loft_different_ratio(secT, secB)
    # only polygon
    pointsB = []
    pointsC = []
    # get total length and step length
    lengthB = get_perimeter_of_section(secB)
    disNum = int(lengthB/20) if int(lengthB/20) >= 50 else 50  # contourline
    stepB = lengthB/disNum
    distLayer = get_distance_of_point_plane(
        get_first_point_on_section(sec2), sec1.transformation)
    layerNum = int(distLayer/20) if int(distLayer/20) >= 10 else 10  # layer
    # process base section
    numSum = 0  # record all number.
    numRec = []  # record every number.
    for i in range(len(segmB)-1):  # catch last fragm
        numI = round(get_perimeter_of_fragment(segmB[i])/stepB)
        pointsI = get_discrete_points_from_fragment(segmB[i], numI, False)
        numRec.append(numI)
        numSum += numI
        pointsB += pointsI
    # processing the last fragment
    numLast = disNum-numSum
    numRec.append(numLast)
    pointsI = get_discrete_points_from_fragment(
        segmB[len(segmB)-1], numLast, True)  # must be close
    pointsB += pointsI
    # process corresponding section
    numSum = 0
    for i in range(len(segmT)-1):  # must particular process last.
        pointsI = get_discrete_points_from_fragment(segmT[i], numRec[i], False)
        pointsC += pointsI
        numSum += numRec[i]
    if len(segmT) == len(segmB):  # while fragments equal
        pointsI = get_discrete_points_from_fragment(
            segmT[len(segmT)-1], numRec[len(segmT)-1], True)
        pointsC += pointsI
    else:
        pointsI = get_discrete_points_from_fragment(
            segmT[len(segmT)-1], numRec[len(segmT)-1], False)
        pointsC += pointsI
        numSum += numRec[len(segmT)-1]
        numLast = disNum-numSum
        pointsC += get_much_offset_points_from_two_points(
            Segment(pointsC[len(pointsC)-1], pointsC[0]), numLast, False)
    # the discrete modeling
    sectionList = []
    for i in range(layerNum+1):  # layer
        pointList = []
        for j in range(disNum):  # contour
            pointJ = pointsB[j]+(i/layerNum)*(pointsC[j]-pointsB[j])
            pointList.append(pointJ)
        pointListU = get_points_on_unified_plane(pointList)
        if is_polygon_self_intersect(pointListU):
            raise ValueError('some lines self-intersect in polygon!')
        sectionList.append(to_section(pointListU))
    geo = Loft(sectionList)
    geo.smooth = True
    return geo


# 点对弧的sweep
def arc_correspond_point_sweep(sec1: Section, sec2: Section) -> Loft:
    # oneside_fillet_sweep
    if len(sec1.parts) != len(sec2.parts):
        raise TypeError("The number of arcs should correspond to points!")
    if all(isinstance(i, Arc) for i in sec1.parts) and is_all_vec(sec2.parts):
        arcSec = sec1
        pointSec = sec2
    elif all(isinstance(i, Arc) for i in sec2.parts) and is_all_vec(sec1.parts):
        arcSec = sec2
        pointSec = sec1
    else:
        raise TypeError("The number of arcs should correspond to points!")
    arcFrag = get_fragments_from_section(arcSec)
    lineFrag = get_fragments_from_section(pointSec)
    discreteNum = 100
    arcSecList = []
    lineSecList = []
    for iter in arcFrag:
        if isinstance(iter, Arc):
            arcList = get_discrete_points_from_arc(iter, discreteNum, True)
            arcSecList += arcList
    for iter in lineFrag:
        points = get_much_offset_points_from_two_points(
            iter.list, discreteNum, True)
        lineSecList += points
    geo = Loft(to_section(arcSecList), to_section(lineSecList))
    geo.smooth = True
    return geo


# ------------------------------------------------------------------------------------------
# |                                        SHOW                                            |
# ------------------------------------------------------------------------------------------


def show_spline_curve(spline: SplineCurve, radius=0, withEnd=True, isShow=True) -> Combine:  # 显示样条线
    geo = Combine()
    peri = get_perimeter_of_spline(spline)
    if radius == 0:
        radius = peri/100
    elif radius > peri/10:
        radius = peri/10
    points = get_discrete_points_from_spline(spline)
    pControl = spline.points
    geo.append(trans(pControl[0])*scale(radius)*Sphere().colorMagenta())
    if withEnd:
        geo.append(trans(pControl[-1])*scale(radius)*Sphere().colorMagenta())
    vecFirst = pControl[1]-pControl[0]
    vecLast = pControl[-1]-pControl[-2]
    arcSec = Arc()
    arcSec.transformation = trans(
        pControl[0])*scale(1/2*radius)*get_matrix_from_one_vector(vecFirst, True)
    pointA = pControl[-1]-radius*unitize(vecLast)  # the vertex of conus
    sigma = 0
    i = -1
    while(sigma < 3*radius):
        sigma += norm(points[i]-points[i-1])
        i = i-1
    arcCon = Arc()
    arcCon.transformation = trans(
        points[i])*scale(radius)*get_matrix_from_one_vector(points[i]-points[i-1], True)
    geo.append(conus_underside_vertex(arcCon, pointA).colorCyan())
    for i in range(abs(i+1)):
        points.pop()
    geo.append(sweep_stere(Section(arcSec), Line(points), True).colorOrange())
    if isShow:
        create_geometry(geo)
    return geo


def show_arc_direction(arcO: Arc, radius=0, withEnd=True, isShow=True) -> Combine:  # 圆弧方向可视化
    geo = Combine()
    axisX = get_matrixs_axisx(arcO.transformation)
    axisY = get_matrixs_axisy(arcO.transformation)
    axisZ = cross(axisX, axisY)
    arc = deepcopy(arcO)
    R = norm(axisX)
    if radius == 0:
        radius = get_perimeter_of_arc(arcO)/25
    elif radius > get_perimeter_of_arc(arcO)/4:
        radius = get_perimeter_of_arc(arcO)/4
    geo.append(trans(arc.pointStart)*scale(radius)*Sphere().colorMagenta())
    if withEnd:
        geo.append(trans(arc.pointEnd)*scale(radius)*Sphere().colorMagenta())
    if arcO.isCircle:
        R = norm(axisX)
        arcSec = Arc()  # the rotate sweep arc.
        arcSec.transformation = trans(
            arc.pointStart)*get_matrix_from_one_vector(arc.vectorTangentS, True)
        arcSec.scale_center(1/2*radius)
        # L=2*R*sin(theta/2) #the relation of radian and chord.
        angleS = 2*asin(sqrt(3)/2*radius/R/2)  # start part
        angleD = 2*asin(radius/R/2)  # arrow part
        arcSw = rotate_arbitrary(
            arc.pointCenter, axisZ, math_sign(arc.scope)*angleS)*arcSec
        arc.scope = arc.scope-math_sign(arc.scope)*(angleS+3*angleD)
        pipe = Sweep(Section(arcSw), Line(arc))
        pointA = rotate_arbitrary(
            arc.pointCenter, axisZ, -math_sign(arc.scope)*angleD)*arcO.pointEnd
        arcSec.scale_center(sqrt(3))
        arcConus = rotate_arbitrary(
            arc.pointCenter, axisZ, arcO.scope-math_sign(arc.scope)*3*angleD)*arcSec
        arrow = conus_underside_vertex(arcConus, pointA)
        geo.append(pipe.colorOrange())
        geo.append(arrow.colorCyan())
    else:
        arcSec = Arc()
        arcSec.transformation = trans(
            arcO.pointStart)*scale(1/2*radius)*get_matrix_from_one_vector(arcO.vectorTangentS, True)
        # arc.scale_center(1/2*radius)
        a, b, thetaL, thetaR = get_arc_rotate_angle_2D(
            inverse_orth(get_orthogonal_matrix(arc.transformation))*arc)
        R = (a+b)/2
        arc.scope = arc.scope-math_sign(arc.scope)*radius/R
        pointA = arc.pointEnd  # the vertex of conus
        arc.scope = arc.scope-math_sign(arc.scope)*2*radius/R
        pointC = arc.pointEnd  # the bottom arc center
        vectorC = arc.vectorTangentE
        arcCon = Arc()
        arcCon.transformation = trans(
            pointC)*scale(radius)*get_matrix_from_one_vector(vectorC, True)
        geo.append(conus_underside_vertex(arcCon, pointA).colorCyan())
        geo.append(sweep_arc(Section(arcSec), Line(arc)).colorOrange())
    if isShow:
        create_geometry(geo)
    return geo


def show_points_curve_line(line: Line, radius=0) -> Combine:  # 显示线组
    parts = get_nested_parts_from_line(line)
    if is_all_vec(parts):
        return show_points_line(parts, radius)
    frags = get_fragments_from_line(line)
    lenList = []
    for iter in frags:
        lenList.append(get_perimeter_of_fragment(iter))
    minR = min(lenList)
    if radius == 0:
        radius = minR/25
    elif radius > minR/4:
        radius = minR/4
    geo = Combine()
    for i in range(len(frags)):
        isEnd = True if (i == len(frags)-1) else False
        if isinstance(frags[i], Segment):
            geo.append(show_points_line(
                [frags[i].start, frags[i].end], radius, isEnd, False))
        elif isinstance(frags[i], Arc):
            geo.append(show_arc_direction(frags[i], radius, isEnd, False))
        elif isinstance(frags[i], SplineCurve):
            geo.append(show_spline_curve(frags[i], radius, isEnd, False))
    create_geometry(geo)
