# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Geometry topological relation 几何拓扑关系
# Author: akingse
# Date: 2022/01
from .pyp3d_calculation import *

# ------------------------------------------------------------------------------------------
# |                                         POINT                                          |
# ------------------------------------------------------------------------------------------


# 判断点在直线上
def is_point_on_line(point: GeVec3d, line: Segment, isLine=True) -> bool:
    if isLine:
        return is_parallel(point-line.start, point-line.end)
    else:
        return is_point_on_segment(point, line) == "POINT_IN" or is_point_on_segment(point, line) == "POINT_END"


# 判断点与线段的关系
def is_point_on_segment(point: GeVec3d, segm: Segment) -> str:
    '''
    # POINT_END  点与线段端点重合
    # POINT_IN  点在线段内
    # POINT_EXTEND  点在线段延长线上
    # POINT_OUT  点不在线段上
    # '''
    # if norm(point-segm.start) * norm(point-segm.end) < PL_A:
    if is_coincident(point, segm.start) or is_coincident(point, segm.end):
        return "POINT_END"
    # norm(cross(point-segm.start, point-segm.end)) < PL_E7:  # parallel
    elif is_parallel(point-segm.start, point-segm.end):
        return "POINT_IN" if(is_two_vectors_same_direction(point-segm.start, point-segm.end) == "DIRECTION_OPPO") else "POINT_EXTEND"
    else:
        return "POINT_OUT"


# 点到直线的距离
def get_distance_of_point_line(point: GeVec3d, line: Segment) -> float:
    # if norm(line.start-line.end) < PL_A:  # norm of line is zero.
    #     return norm(point-line.start)
    # pt = get_nearest_point_of_point_line(point, line)
    # return norm(pt-to_vec3(point))
    # A = line.start
    # B = line.end
    C = line.start-point
    vec = line.vector
    if is_coincident(line.start, line.end):
        return norm(point-line.start)
    return norm(C+dot(-1.0*vec, C)/dot(vec, vec)*vec)


# 获取点距公式中的点
def get_nearest_point_of_point_line(point: GeVec3d, line: Segment) -> GeVec3d:
    # a point on line that make the minimum distance
    # line0 = to_vec3(line.start)
    # line1 = to_vec3(line.end)
    # if norm(cross(point-line.start, point-line.end)) < PL_A:  # parallel
    if is_parallel(point-line.start, point-line.end):  # parallel
        return point
    # if norm(line1-line0) < PL_A:  # norm of line is zero.
    #     return line0
    a = line.norm*line.norm  # norm(line0-line1)**2
    b = dot(-1.0*line.vector, line.start-point)
    return line.start+(b/a)*line.vector


# 判断点与圆弧的关系
def is_point_on_arc(point: GeVec3d, arc: Arc, is2D=False) -> str:
    '''
    # POINT_ON  点在圆弧上
    # POINT_EXTEND  点在圆弧延长线上
    # POINT_END  点与圆弧端点重合
    # POINT_IN  点在圆弧(所在圆)内
    # POINT_OUT  点在圆弧(所在圆)外
    # POINT_NOTCO  点与圆弧不共面
    '''
    mat = arc.transformation
    if is2D and is_shadow_matrix_on_xoy(mat):
        mat = get_full_rank_matrix_from_shadow(mat, True)
        # arcN = matN*Arc()
        # arcN.scope = arc.scope
    if not is_point_on_plane(point, get_orthogonal_matrix(mat)):
        return "POINT_NOTCO"
    invM = inverse(mat)
    relaP = invM*to_vec3(point)
    d = norm(relaP)
    if abs(d-1) < PL_A:  # point on arc
        if abs(arc.scope-2*pi) < PL_A:  # to using less calculate.
            return "POINT_ON"
        # theta with math_sign.
        theta = get_angle_of_two_vectors(g_axisX, relaP, False)
        if abs(theta) < PL_A or abs(theta-arc.scope) < PL_A:
            return "POINT_END"
        if arc.scope > 0 and theta < 0:
            theta = angle_posi(theta)
        elif arc.scope < 0 and theta > 0:
            theta = angle_nega(theta)
        if (theta-arc.scope)*(theta) < 0:
            return "POINT_ON"
        else:
            return "POINT_EXTEND"  # on extend line
    elif d < 1:
        return "POINT_IN"
    else:
        return "POINT_OUT"


# ------------------------------------------------------------------------------------------
# |                                        LINE                                            |
# ------------------------------------------------------------------------------------------


# 直线（线段）与直线（线段）的关系
def is_two_line_intersect(lineA: Segment, lineB: Segment, isLineA=False, isLineB=False) -> str:
    # if norm(lineA[1]-lineA[0])*norm(lineB[1]-lineB[0]) < PL_A:  # zero norm
    #     return "LINES_ZERO"
    # different planes
    if not (is_points_on_same_plane([lineA.start, lineA.end, lineB.start, lineB.end])):
        return "LINES_NONCOP"
    # 两条直线的关系
    if isLineA and isLineB:
        # LINES_PARA 平行
        # LINES_COLLINE 共线
        # LINES_INTER 相交
        if is_parallel(lineA.vectorU, lineB.vectorU):  # parallel
            return "LINES_COLLINE" if (is_parallel(lineA.start-lineB.start, lineA.start-lineB.end)) else "LINES_PARA"
        else:
            return "LINES_INTER"
    # 两条线段的关系
    if (not isLineA) and (not isLineB):
        # SEGMENTS_PARALLEL_H, //平行-H形（平行相离）
        # SEGMENTS_PARALLEL_I, //平行-I形（共线相接）
        # SEGMENTS_PARALLEL_C, //平行-C形（共线相交）
        # SEGMENTS_PARALLEL_i, //平行-i形（共线相离）
        # SEGMENTS_INTERSECT_V, //相交-V形（相接/垂直）
        # SEGMENTS_INTERSECT_T, //相交-T形
        # SEGMENTS_INTERSECT_X, //相交-X形
        # SEGMENTS_SEPARATE,    //共面相离
        if (is_parallel(lineA.vectorU, lineB.vectorU)):  # parallel
            if (is_parallel(lineB.start-lineA.start, lineB.start-lineA.end)):  # not parallel
                return "PARALLEL_H"  # 平行-H
            elif is_point_on_segment(lineA.start, lineB) == "POINT_EXTEND" and is_point_on_segment(lineA.end, lineB) == "POINT_EXTEND":
                return "PARALLEL_i"  # 平行-i
            elif is_point_on_segment(lineA.start, lineB) == "POINT_END" or is_point_on_segment(lineA.end, lineB) == "POINT_END":
                return "PARALLEL_I"  # 平行-I
            else:
                return "PARALLEL_C"
        else:
            point = get_intersect_point_of_two_lines(lineA, lineB)[
                0]  # intersect
            if is_point_on_segment(point, lineA) == "POINT_IN" and is_point_on_segment(point, lineB) == "POINT_IN":
                return "INTERSECT_X"  # 相交-X形
            elif is_point_on_segment(point, lineA) == "POINT_IN" or is_point_on_segment(point, lineB) == "POINT_IN":
                return "INTERSECT_T"  # 相交-T形
            elif is_point_on_segment(point, lineA) == "POINT_END" and is_point_on_segment(point, lineB) == "POINT_END":
                return "INTERSECT_V"  # 相交-V形
            else:
                return "SEPARATE"
    # 直线与线段的关系 (isLineA ^ isLineB)
    # SEGMENT_COLLINE //两线共线
    # SEGMENT_END //直线过线段端点
    # SEGMENT_INTER //直线穿过线段
    # SEGMENT_SEPA //相离
    elif isLineA and (not isLineB):
        line0 = lineA.start
        line1 = lineA.end
        segm0 = lineB.start
        segm1 = lineB.end
    elif (not isLineA) and isLineB:
        segm0 = lineA.start
        segm1 = lineA.end
        line0 = lineB.start
        line1 = lineB.end
    if (is_parallel(segm0-line0, segm0-line1)) and (is_parallel(segm1-line0, segm1-line1)):
        return "SEGMENT_COLLINE"  # line on line
    elif (is_parallel(segm0-line0, segm0-line1)) or (is_parallel(segm1-line0, segm1-line1)):
        return "SEGMENT_END"  # line through the segments end point
    # using single straddle experiment
    stra = dot(cross(segm0-line0, segm1-segm0),
               cross(segm1-line0, segm1-segm0))
    maxl = max(norm(segm0), norm(segm1), norm(line0), norm(line1))+1
    return "SEGMENT_INTER" if (abs(stra) < maxl*PL_A or stra <= 0) else "SEGMENT_SEPA"


# 两条线段分离的快速算法
def is_two_segments_intersect_2D(segmA: Segment, segmB: Segment, ignoreZero=True) -> bool:
    p1 = segmA.start
    p2 = segmA.end
    p3 = segmB.start
    p4 = segmB.end
    # is zero verctor regard as intersect.
    if ignoreZero and (is_coincident(p2, p1) or is_coincident(p4, p3)):
        return False
    # fast mutual exclusion
    if min(p1.x, p2.x) > max(p3.x, p4.x) or min(p3.y, p4.y) > max(p1.y, p2.y) or \
            min(p3.x, p4.x) > max(p1.x, p2.x) or min(p1.y, p2.y) > max(p3.y, p4.y):
        return False
    # double straddle experiment
    straA = dot(cross(p1-p3, p4-p3), cross(p2-p3, p4-p3))
    straB = dot(cross(p4-p1, p2-p1), cross(p3-p1, p2-p1))
    maxl = max(norm(p1), norm(p2), norm(p3), norm(p4))+1
    # straA<maxl*PL_A
    return (abs(straA) < maxl*PL_A or straA <= 0) and (abs(straB) < maxl*PL_A or straB <= 0)
    # first veision
    # if norm(cross(p2-p1, p4-p3))<PL_E8 and norm(cross(p3-p1, p3-p2))<PL_E8 : # collinear
    #     return True if (dot(p3-p1, p3-p2)<=0 or dot(p4-p1, p4-p2)<=0) else False
    # A1,B1,C1=get_coefficients_from_two_points(p1,p2)
    # A2,B2,C2=get_coefficients_from_two_points(p3,p4)
    # k1=(A1*p3.x+B1*p3.y+C1)*(A1*p4.x+B1*p4.y+C1)
    # k2=(A2*p1.x+B2*p1.y+C2)*(A2*p2.x+B2*p2.y+C2)
    # return True if (k1<=0 or abs(k1)<PL_A) and (k2<=0 or abs(k2)<PL_A) else False


# 空间（异面）直线间的距离
def get_distance_of_two_lines(lineA: Segment, lineB: Segment) -> float:
    if is_points_on_same_plane([lineA.start, lineA.end, lineB.start, lineB.end]):  # coplanar
        # if norm(lineA[0]-lineA[1])*norm(lineA[0]-lineA[1]) < PL_A:  # some zero vector
        #     d1 = get_distance_of_point_line(lineA.start, [lineB[0], lineB[1]])
        #     d2 = get_distance_of_point_line(lineA.end, [lineB[0], lineB[1]])
        #     if abs(d1-d2) < PL_A: return d1
        #     else: return get_distance_of_point_line(lineB.start, [lineA[0], lineA[1]])
        if (is_parallel(lineA.vectorU, lineB.vectorU)):  # parallel
            return get_distance_of_point_line(lineA.start, lineB)
        else:
            return 0.0
    else:  # different planes
        matA = get_matrix_from_one_vector(lineA.vectorU, True)
        point3 = inverse_orth(matA)*lineB.start
        point4 = inverse_orth(matA)*lineB.end
        # if abs(point3.z-point4.z)<PL_A: # vertical
        return get_distance_of_point_line(g_axisO, Segment(point3, point4))


# 平面中直线夹角
def get_angle_of_two_segments(segmA: Segment, segmB: Segment) -> float:
    if isinstance(segmA, Segment) and isinstance(segmB, Segment):
        return get_angle_of_two_vectors(segmA.vectorU, segmB.vectorU)
    else:  # both list
        return get_angle_of_two_vectors(segmA[1]-segmA[0], segmB[1]-segmB[0])
#     return atan2(norm(cross(lineA.vector, lineB.vector)), dot(lineA.vector, lineB.vector))
#     return atan2(norm(cross(lineA[1]-lineA[0], lineB[1]-lineB[0])), dot(lineA[1]-lineA[0], lineB[1]-lineB[0]))


# 获取两直线交点的列表
def get_intersect_point_of_two_lines(lineA: Segment, lineB: Segment, isLineA=False, isLineB=False) -> list:
    if not is_points_on_same_plane([lineA.start, lineA.end, lineB.start, lineB.end]):
        return []
    pointInter = []
    if is_parallel(lineA.vector, lineB.vector):  # parallel
        if is_parallel(lineA.start-lineB.start, lineA.start-lineB.end):  # collinear
            pointInter = [lineA.start, lineA.end]
    else:
        A = lineA.vector  # B-A
        B = lineB.vector  # D-C
        C = lineA.start - lineB.start  # u=A-C
        a = A*B*A*B-A*A*B*B
        b = C*B*A*B-C*A*B*B
        pointInter = [lineA.start-b/a*A]
        # pvA = to_pos_vec(lineA)
        # pvB = to_pos_vec(lineB)
        # pointInter = [
        #     pvB.pos+norm(cross(pvA.vec, pvB.pos-pvA.pos))/norm(cross(pvA.vec, pvB.vec))*pvB.vec]
    # if isLineA and isLineB:
    #     return pointInter
    # else:
    pointsIn = []
    for iter in pointInter:
        if isLineA and isLineB:  # line and line
            pointsIn.append(iter)
        if isLineA and (not isLineB):  # line and segment
            if (is_point_on_segment(iter, lineB) == "POINT_IN" or is_point_on_segment(iter, lineB) == "POINT_END"):
                pointsIn.append(iter)
        elif (not isLineA) and isLineB:  # segment and line
            if (is_point_on_segment(iter, lineA) == "POINT_IN" or is_point_on_segment(iter, lineA) == "POINT_END"):
                pointsIn.append(iter)
        else:  # segment and segment
            if (is_point_on_segment(iter, lineB) == "POINT_IN" or is_point_on_segment(iter, lineB) == "POINT_END") and\
                    (is_point_on_segment(iter, lineA) == "POINT_IN" or is_point_on_segment(iter, lineA) == "POINT_END"):
                pointsIn.append(iter)
    return pointsIn


# Arc

# 直线（线段）与圆弧的关系
def is_line_arc_intersect(line: Segment, arc: Arc, isLine=False, isCircle=False) -> str:
    '''
    # NONPLANAR 不共面（相交-相离）
    # LINE_ARC_TANGEN 相切
    # LINE_ARC_INTER 相交(circle-2)
    # LINE_ARC_SEPA 相离
    '''
    forwM = arc.transformation
    if is_line_locate_on_plane(line, forwM) != "LINE_ON":
        return "NONPLANAR"
    if isLine and isCircle:
        lineRela = inverse(forwM)*line
        d = get_distance_of_point_line(g_axisO, lineRela)
        if abs(d-1) < PL_A:
            return "LINE_ARC_TANGEN"
        elif d < 1:
            return "LINE_ARC_INTER"
        else:
            return "LINE_ARC_SEPA"
    else:
        points = get_intersect_point_of_line_arc(line, arc, isLine, isCircle)
        return "LINE_ARC_INTER" if(len(points) >= 1) else "LINE_ARC_SEPA"


# 获取直线和圆弧的交点
def get_intersect_point_of_line_arc(line: Segment, arc: Arc, isLine=False, isCircle=False) -> list:
    forwM = arc.transformation
    if is_line_locate_on_plane(line, forwM) == "LINE_PARA":  # parallel separate
        return []
    elif is_line_locate_on_plane(line, forwM) == "LINE_VERTI" or is_line_locate_on_plane(line, forwM) == "LINE_INTER":  # intersect
        pointI = get_intersect_point_of_line_plane(line, forwM, True)[0]
        if isCircle:
            return [pointI] if (is_point_on_arc(pointI, arc) == "POINT_ON" or is_point_on_arc(pointI, arc) == "POINT_END" or
                                is_point_on_arc(pointI, arc) == "POINT_EXTEND") else []
        else:
            return [pointI] if (is_point_on_arc(pointI, arc) == "POINT_ON" or is_point_on_arc(pointI, arc) == "POINT_END") else []
    # line on arc plane
    invM = inverse(forwM)  # get the unit arc
    lineA = invM*line
    theta = get_angle_of_two_vectors(g_axisX, lineA.vectorU)
    lineR = rotz(-theta)*lineA
    py = lineR.start.y  # transfer to horizontal line
    p1 = GeVec3d(sqrt(1-py*py), py)
    p2 = GeVec3d(-sqrt(1-py*py), py)
    pointsI = forwM*rotz(theta)*[p1, p2]  # nice alg
    if isLine and isCircle:  # line and circle
        return pointsI
    pointsIn = []  # to differentiate whether or not full arc
    for iter in pointsI:
        if isLine and (not isCircle):  # line and arc
            if is_point_on_arc(iter, arc) == "POINT_ON" or is_point_on_arc(iter, arc) == "POINT_END":
                pointsIn.append(iter)
        elif (not isLine) and isCircle:  # segment and circle
            if is_point_on_segment(iter, line) == "POINT_IN" or is_point_on_segment(iter, line) == "POINT_END":
                pointsIn.append(iter)
        else:  # segment and arc
            if (is_point_on_arc(iter, arc) == "POINT_ON" or is_point_on_arc(iter, arc) == "POINT_END") and\
                    (is_point_on_segment(iter, line) == "POINT_IN" or is_point_on_segment(iter, line) == "POINT_END"):
                pointsIn.append(iter)
    return pointsIn


# 两个圆弧之间的关系
def is_two_arcs_intersect(arc1: Arc, arc2: Arc, isBothCircle=False) -> str:
    '''
    # ARCS_INTER 相交
    # ARCS_TANGEN 相切
    # ARCS_SEPA 相离
    '''
    if isBothCircle:
        points = get_intersect_point_of_two_arcs(arc1, arc2, True)
        if len(points) == 0:
            return "ARCS_SEPA"
        elif len(points) == 1:
            return "ARCS_TANGEN"
        else:
            return "ARCS_INTER"
    else:
        points = get_intersect_point_of_two_arcs(arc1, arc2, False)
        return "ARCS_INTER" if(len(points) >= 1) else "ARCS_SEPA"


# 椭圆与椭圆交点
def get_intersect_point_of_two_arcs(arc1: Arc, arc2: Arc, isBothCircle=False) -> list:
    mat1 = arc1.transformation
    axis1x = get_matrixs_axisx(mat1)
    axis1y = get_matrixs_axisy(mat1)
    mat2 = arc2.transformation
    axis2x = get_matrixs_axisx(mat2)
    axis2y = get_matrixs_axisy(mat2)
    if not (abs(dot(axis1x, axis1y)) < PL_A and abs(dot(axis2x, axis2y)) < PL_A):
        # only using for orthogonal oval, not sheared oval.
        raise TypeError('unsupported oval type!')
    if is_two_planes_intersect(mat1, mat2) != "PLANES_COPLANAR":  # not coplanar
        return []
    forwM = get_orthogonal_matrix(mat1, True)
    arcRela2 = inverse_orth(forwM)*arc2
    # standard oral formula
    A, B, thetaL, thetaR = get_arc_rotate_angle_2D(arc1, True)
    # A, B, angle = get_arc_axis_and_angle(arc1)
    a, b, c, d, e = get_coefficients_from_arc(arcRela2)
    Ac = ((1 - (B**2*b)/A**2)**2 + (B**2*a**2)/A**2)  # x**4
    Bc = ((2*B**2*a*d)/A**2 - 2*c*((B**2*b)/A**2 - 1))  # x**3
    Cc = (c**2 - B**2*a**2 - 2*(b*B**2 + e) *
          ((B**2*b)/A**2 - 1) + (B**2*d**2)/A**2)  # x**2
    Dc = (2*c*(b*B**2 + e) - 2*B**2*a*d)  # x
    Ec = (b*B**2 + e)**2 - B**2*d**2
    xList = math_ferrari_formula(Ac, Bc, Cc, Dc, Ec)
    points = []
    for x in xList:
        under = B**2*(1-x**2/A**2)
        if under >= 0:
            y1 = sqrt(under)
            y2 = -y1
            if abs(x**2+a*x*y1+b*y1**2+c*x+d*y1+e) < PL_E6:  # is point on circle
                points.append(forwM*GeVec3d(x, y1))
            if abs(x**2+a*x*y2+b*y2**2+c*x+d*y2+e) < PL_E6:
                points.append(forwM*GeVec3d(x, y2))
    points = remove_coincident_point(points, True)
    # return points
    if isBothCircle:
        return points
    else:
        pointsArc = []
        for iter in points:
            if (is_point_on_arc(iter, arc1) == "POINT_ON" or is_point_on_arc(iter, arc1) == "POINT_END") and \
                    (is_point_on_arc(iter, arc2) == "POINT_ON" or is_point_on_arc(iter, arc2) == "POINT_END"):
                pointsArc.append(iter)
        return pointsArc


# spline


# 直线与样条线的交点
def get_intersect_point_of_line_spline(line: Segment, spline: SplineCurve, isLine=False) -> list:
    cPoints = spline.transformation*spline.points
    segmsC = get_segments_from_points(cPoints)
    cPoints += [line.start, line.end]
    # using control points to preprocessing
    if is_points_on_same_plane(cPoints):
        points = []
        for iter in segmsC:
            points += get_intersect_point_of_two_lines(
                line, iter, isLine, False)
        if len(points) == 0:
            return []
    pointI = []  # points intersect list
    disPoints = get_discrete_points_from_spline(spline)
    segms = get_segments_from_points(disPoints)
    for iter in segms:
        pointI += get_intersect_point_of_two_lines(line, iter, isLine, False)
    return pointI


# 圆弧与样条线的交点
def get_intersect_point_of_arc_spline(arc: Arc, spline: SplineCurve, isCircle=False) -> list:
    points = get_discrete_points_from_spline(spline)
    segms = get_segments_from_points(points)
    pointInter = []
    for iter in segms:
        pointI = get_intersect_point_of_line_arc(iter, arc, False, isCircle)
        pointInter += pointI
    return pointInter


# 样条线与样条线的交点
def get_intersect_point_of_two_splines(splineA: SplineCurve, splineB: SplineCurve) -> list:
    segmsA = get_segments_from_points(get_discrete_points_from_spline(splineA))
    segmsB = get_segments_from_points(get_discrete_points_from_spline(splineB))
    pointInter = []
    for iterA in segmsA:
        for iterB in segmsB:
            pointI = get_intersect_point_of_two_lines(
                iterA, iterB, False, False)
            pointInter += pointI
    return pointInter


# ------------------------------------------------------------------------------------------
# |                                         PLANE                                          |
# ------------------------------------------------------------------------------------------


# 两个正交矩阵的关系
def is_two_planes_intersect(planeO: GeTransform, planeA: GeTransform) -> str:
    '''
    # using for judge the ralation of two planes and two arcs.
    # PLANES_PARALLEL, //两面平行（相离）
    # PLANES_COPLANAR, //两面共面（重合）
    # PLANES_INTERSECT, //两面相交（不垂直）
    # PLANES_VERTICAL, //两面垂直（z轴夹角pi/2）
    '''
    axisZ = get_matrixs_axisz(get_orthogonal_matrix(planeO))
    axisO = get_matrixs_position(planeO)
    vecX = get_matrixs_axisx(planeA)
    vecY = get_matrixs_axisy(planeA)
    vecZ = cross(vecX, vecY)
    vecO = get_matrixs_position(planeA)
    if (is_perpendi(vecX, axisZ) and is_perpendi(vecY, axisZ)):
        return "PLANES_COPLANAR" if (is_perpendi((vecO-axisO), axisZ)) else "PLANES_PARALLEL"
    else:
        return "PLANES_INTERSECT" if(is_perpendi(vecZ, axisZ)) else "PLANES_VERTICAL"


# (平行)平面间的距离
def get_distance_of_two_planes(planeA: GeTransform, planeB: GeTransform) -> float:
    matA = get_orthogonal_matrix(planeA)  # orthogonal matrix
    matB = get_orthogonal_matrix(planeB)
    relaB = inverse(matA)*matB
    if not is_two_dimensional_matrix(get_matrixs_rotation(relaB)):
        return 0.0
    else:
        return abs(get_matrixs_position(relaB).z)


# 平面之间的夹角
def get_angle_of_two_planes(planeA: GeTransform, planeB: GeTransform) -> float:
    veczA = get_matrixs_axisz(planeA)
    veczB = get_matrixs_axisz(planeB)
    angle = get_angle_of_two_vectors(veczA, veczB, True)  # always be positive
    return pi-angle


# 两平面的交线
def get_intersect_line_of_two_planes(planeB: GeTransform, planeS: GeTransform) -> list:
    planeB = get_orthogonal_matrix(planeB)  # base plane
    planeS = get_orthogonal_matrix(planeS)  # shadow axis plane
    axisO = get_matrixs_position(planeS)
    if is_two_planes_intersect(planeB, planeS) == "PLANES_COPLANAR":
        return [axisO, axisO+get_matrixs_axisx(planeS), axisO+get_matrixs_axisy(planeS)]
    elif is_two_planes_intersect(planeB, planeS) == "PLANES_PARALLEL":
        return []
    else:  # two planes intersect
        lineX = Segment(axisO, axisO+get_matrixs_axisx(planeS))
        lineY = Segment(axisO, axisO+get_matrixs_axisy(planeS))
        # planeS original point loacad on planeB
        if is_point_on_plane(axisO, planeB):
            if is_line_locate_on_plane(lineX, planeB) == "LINE_ON":
                return [axisO, axisO+lineX.vectorU]
            elif is_line_locate_on_plane(lineY, planeB) == "LINE_ON":
                return [axisO, axisO+lineY.vectorU]
            else:
                planeS = planeS*trans(g_axisX)  # trans g_axisX of planeS
                # refresh param of planes
                axisO = get_matrixs_position(planeS)
                lineX = Segment(axisO, axisO+get_matrixs_axisx(planeS))
                lineY = Segment(axisO, axisO+get_matrixs_axisy(planeS))
        # lineX/lineY isnot parallel to planeB
        # elif is_line_locate_on_plane(lineX,planeB)=="LINE_PARA" or is_line_locate_on_plane(lineY,planeB)=="LINE_PARA":
        #     planeS = planeS*rotz(pi/4) #arbitrary_rotate(axisO,get_matrixs_axisz(planeS),pi/4)*planeS
        # lineX=Segment(axisO,axisO+get_matrixs_axisx(planeS)) # re assign lineX/lineY
        # lineY=Segment(axisO,axisO+get_matrixs_axisy(planeS))
        # while lineX parallel to planeB, move g_axisX to move axisO
        elif is_line_locate_on_plane(lineX, planeB) == "LINE_PARA":
            planeS2 = planeS*trans(g_axisX)
            axisO = get_matrixs_position(planeS2)
            lineY2 = Segment(axisO, axisO+get_matrixs_axisx(planeS2))
            return [get_intersect_point_of_line_plane(lineY, planeB, True)[0], get_intersect_point_of_line_plane(lineY2, planeB, True)[0]]
        elif is_line_locate_on_plane(lineY, planeB) == "LINE_PARA":
            planeS2 = planeS*trans(g_axisY)
            axisO = get_matrixs_position(planeS2)
            lineX2 = Segment(axisO, axisO+get_matrixs_axisx(planeS2))
            return [get_intersect_point_of_line_plane(lineX, planeB, True)[0], get_intersect_point_of_line_plane(lineX2, planeB, True)[0]]
        return [get_intersect_point_of_line_plane(lineX, planeB, True)[0], get_intersect_point_of_line_plane(lineY, planeB, True)[0]]


# relation and intersect point of plane


# 直线（线段）与平面的关系
def is_line_locate_on_plane(line: Segment, plane: GeTransform, isLine=False) -> str:
    '''
    # LINE_ON  在面上
    # LINE_PARA  与面平行
    # LINE_INTER  与面相交（包含端点相接）
    # LINE_SEPA  与面分离
    '''
    p0 = line.start
    p1 = line.end
    mat = get_orthogonal_matrix(plane)
    axisZ = get_matrixs_axisz(mat)
    if is_perpendi(p1-p0, axisZ):  # line plane parallel, perpendi to normal-vector
        return "LINE_ON" if is_point_on_plane(p0, plane) else "LINE_PARA"
    else:  # return "LINE_VERTI" if norm(cross(p0-p1, axisZ))<PL_A else "LINE_INTER"
        if isLine:
            return "LINE_INTER"
        else:
            p0 = inverse_orth(mat)*p0
            p1 = inverse_orth(mat)*p1
            return "LINE_INTER" if (p0.z*p1.z <= 0) else "LINE_SEPA"


# 直线（线段）与平面的交点
def get_intersect_point_of_line_plane(line: Segment, plane: GeTransform, isLine=False) -> list:
    if is_line_locate_on_plane(line, plane) == "LINE_ON":  # line on plane
        return [line.start, line.end]
    elif is_line_locate_on_plane(line, plane) == "LINE_PARA":  # parallel but separate
        return []
    else:  # not using coord_system transfer, to decrease calculate
        vecZ = get_matrixs_axisz(get_orthogonal_matrix(plane))
        pO = get_matrixs_position(plane)
        p0 = line.start
        p1 = line.end
        k = dot(vecZ, p0-pO)/dot(vecZ, p0-p1)
        pointI = p0+k*(p1-p0)  # paramater formula vector
        if isLine:
            return [pointI]
        else:
            return [pointI] if (is_point_on_segment(pointI, line) == "POINT_IN" or
                                is_point_on_segment(pointI, line) == "POINT_END") else []


# 圆弧与平面的关系
def is_arc_locate_on_plane(arc: Arc, plane: GeTransform, isCircle=False) -> str:
    '''
    # ARC_COPLANAR, //圆在平面上
    # ARC_PARALLEL, //圆与平面平行（相离）
    # ARC_INTERSECT, //圆与平面相交
    # ARC_SEPARATE, //圆与平面相离（不平行）
    # ARC_TANGENT, //圆与平面相切
    '''
    matArc = arc.transformation
    if is_two_planes_intersect(matArc, plane) == "PLANES_COPLANAR":
        return "ARC_COPLANAR"
    elif is_two_planes_intersect(matArc, plane) == "PLANES_PARALLEL":
        return "ARC_PARALLEL"
    else:
        points = get_intersect_point_of_arc_plane(arc, plane, isCircle)
        return "ARC_INTERSECT" if (len(points) >= 1) else "ARC_SEPARATE"


# 圆弧与平面的交点
def get_intersect_point_of_arc_plane(arc: Arc, plane: GeTransform, isCircle=False) -> list:
    matArc = arc.transformation
    if is_two_planes_intersect(matArc, plane) == "PLANES_COPLANAR":
        return get_three_points_from_arc(arc)  # while coplanar return 3 points
    elif is_two_planes_intersect(matArc, plane) == "PLANES_PARALLEL":
        return []
    else:
        segm = to_segment(get_intersect_line_of_two_planes(
            matArc, plane))  # orthogonal in next function
        pointI = get_intersect_point_of_line_arc(
            segm, arc, True, True)  # intersect point of full arc.
        if isCircle:  # full arc
            return pointI
        else:
            pointArc = []  # choose the point that intersect with plane
            for p in pointI:
                if is_point_on_arc(p, arc):
                    pointArc.append(p)
            return pointArc


# 样条线与平面的关系
def is_spline_locate_on_plane(spline: SplineCurve, plane: GeTransform) -> str:
    '''
    # SPLINE_3D, //三维spline
    # SPLINE_ON, //spline在平面上
    # SPLINE_PARA, //spline与平面平行
    # SPLINE_INTER, //spline与平面相交
    # SPLINE_SEPA, //圆与平面相离（不平行）
    '''
    points = spline.transformation*spline.points  # using control points
    if not is_points_on_same_plane(points):
        return "SPLINE_3D"
    matS = get_matrix_from_points(points)
    if is_two_planes_intersect(matS, plane) == "PLANES_COPLANAR":
        return "SPLINE_ON"
    elif is_two_planes_intersect(matS, plane) == "PLANES_PARALLEL":
        return "SPLINE_PARA"
    else:
        segms = get_segments_from_points(points)
        for segm in segms:
            if is_line_locate_on_plane(segm, plane) == "LINE_INTER":
                return "SPLINE_INTER"
        return "SPLINE_SEPA"


# 样条线与平面的交点
def get_intersect_point_of_spline_plane(spline: SplineCurve, plane: GeTransform) -> list:
    points = get_discrete_points_from_spline(spline)
    segms = get_segments_from_points(points)
    pointInter = []
    for iter in segms:
        pointI = get_intersect_point_of_line_plane(iter, plane)
        pointInter += pointI
    return pointInter


# 两个fragments的交点
def get_intersect_points_of_fragments(para1, para2) -> list:
    '''
    # 线段-线段 segm1-segm2
    # 线段-圆弧 segm-arc
    # 线段-样条线 segm-spline
    # 圆弧-圆弧 arc1-arc2
    # 圆弧-样条线 arc-spline
    # 样条线-样条线 spline1-spline2
    '''
    if isinstance(para1, Segment) and isinstance(para2, Segment):
        return get_intersect_point_of_two_lines(para1, para2, False, False)
    elif (isinstance(para1, Segment) and isinstance(para2, Arc)):
        return get_intersect_point_of_line_arc(para1, para2, False, False)
    elif (isinstance(para2, Segment) and isinstance(para1, SplineCurve)):
        return get_intersect_point_of_line_spline(para1, para2, False)
    elif isinstance(para1, Arc) and isinstance(para2, Arc):
        return get_intersect_point_of_two_arcs(para1, para2, False)
    elif (isinstance(para1, Arc) and isinstance(para2, SplineCurve)):
        return get_intersect_point_of_arc_spline(para1, para2, False)
    elif (isinstance(para2, SplineCurve) and isinstance(para1, SplineCurve)):
        return get_intersect_point_of_two_splines(para1, para2)
    else:
        raise TypeError('fragments parameters error!')


# ------------------------------------------------------------------------------------------
# |                                       POLYGON                                          |
# ------------------------------------------------------------------------------------------


# 判断点是否在多边形上
def is_point_on_polygon(point: GeVec3d, polygon: list) -> bool:
    segments = get_segments_from_points(
        polygon, True, True)  # polygon must close
    for segm in segments:
        if is_point_on_segment(point, segm) == "POINT_IN" or is_point_on_segment(point, segm) == "POINT_END":
            return True
    return False


# 判断点是否在多边形内
def is_point_in_polygon(point: GeVec3d, polygon: list) -> bool:
    # after shallow copy, donot using original object.
    pointJ = copy.deepcopy(polygon)
    pointJ.append(point)
    if not is_points_on_same_plane(pointJ):
        return False
    if is_point_on_polygon(point, polygon):
        return True
    mat = get_matrix_from_points(polygon, True)
    polygon = inverse(mat)*polygon  # transfer to XoY plane to process.
    point = inverse(mat)*point
    rangeP = get_range_of_polygon(polygon)
    if point.x < rangeP[0] or point.x > rangeP[1] or point.y < rangeP[2] or point.y > rangeP[3]:  # out of range
        return False
    # ray-crossing method:
    isIn = False
    j = len(polygon)-1
    for i in range(len(polygon)):
        if ((polygon[i].y > point.y) != (polygon[j].y > point.y)) and \
                ((point.x-polygon[i].x) < (polygon[j].x-polygon[i].x)*(point.y-polygon[i].y)/(polygon[j].y-polygon[i].y)):
            isIn = bool(1-isIn)  # b=!b
        j = i
    return isIn


# 点是否在轮廓线上
def is_point_on_contourline(point: GeVec3d, line: Section) -> bool:
    frag = get_fragments_from_section(line)
    for iter in frag:
        if isinstance(iter, Segment):
            if is_point_on_segment(point, iter) == "POINT_IN" or is_point_on_segment(point, iter) == "POINT_END":
                return True
        elif isinstance(iter, Arc):
            if is_point_on_arc(point, iter) == "POINT_ON" or is_point_on_arc(point, iter) == "POINT_END":
                return True
        # elif isinstance(iter, SplineCurve):
        #     return True
        else:
            raise TypeError('parameter type error!')
    return False


# 点在截面内（或截面轮廓线上）
def is_point_in_contourline(point: GeVec3d, sec: Section) -> bool:
    if isinstance(sec, Fusion):  # better fusion union
        # attention, using 2D section
        pRela = inverse(sec.transformation)*point
        for iter in sec.parts:
            if is_point_on_contourline(pRela, iter):
                return True
            points = get_discrete_points_from_section(sec)
            if is_point_in_polygon(pRela, points):
                return True
        return False
    elif isinstance(sec, Section):
        if is_point_on_contourline(point, sec):
            return True
        points = get_discrete_points_from_section(sec)
        return is_point_in_polygon(point, points)
    else:
        return False


# 多边形是否自相交
def is_polygon_self_intersect(points: list) -> bool:
    if not is_points_on_same_plane(points):
        raise TypeError("points arenot on same plane!")
    points = copy.deepcopy(points)
    invM = inverse_orth(get_matrix_from_points(points))
    points = invM*points
    # already remove coincident point
    segms = get_segments_from_points(points, True, True)
    lenL = len(segms)
    # if lenL<=2:
    for i in range(2, lenL-1):  # first segment
        if is_two_segments_intersect_2D(segms[0], segms[i], True):
            return True
    for i in range(1, lenL):
        for j in range(i+2, lenL):  # range cannot from big to small
            if is_two_segments_intersect_2D(segms[i], segms[j], True):
                return True
    return False


# 轮廓线是否自相交
def is_contourline_self_intersect(line: Line) -> str:
    '''
    # NOT_COPLANAR 不共面
    # BACK_LINE 回头线
    # SELF_INTER 有自相交
    # EACH_SEPA 互相分离
    '''
    if is_line_on_same_plane(line):
        return "NOT_COPLANAR"
    frags = get_fragments_from_line(line)
    lenL = len(frags)
    if lenL == 2:
        points = get_intersect_points_of_fragments(frags[0], frags[1])
        if len(points) >= 1:
            return "SELF_INTER"
    for i in range(2, lenL-1):  # first segment
        if get_intersect_points_of_fragments(frags[0], frags[i]):
            if len(points) >= 1:
                return "SELF_INTER"
    for i in range(1, lenL):
        for j in range(i+2, lenL):  # range cannot from big to small
            if get_intersect_points_of_fragments(frags[i], frags[j]):
                if len(points) >= 1:
                    return "SELF_INTER"
    return "EACH_SEPA"


# 判断两个截面是否有相交的部分
def is_two_sections_intersect(secA: Section, secB: Section) -> str:
    '''
    # COPLANAR_INTER 共面-相交（相接）
    # COPLANAR_SEPA 共面-相离
    # NOT_COPLANAR_INTER 异面-相交（相接）
    # NOT_COPLANAR_SEPA 异面-相离（平行）
    '''
    matA = get_matrix_from_section(secA)
    matB = get_matrix_from_section(secB)
    # base section, discrete to be polygon.
    polygonA = get_discrete_points_from_section(secA)
    polygonB = get_discrete_points_from_section(secB)
    # get intersect of frag and matA, judeg is intersect point in polygon.
    fragsB = get_fragments_from_section(secB)
    fragsA = get_fragments_from_section(secA)
    if is_two_planes_intersect(matA, matB) == "PLANES_PARALLEL":
        return "NOT_COPLANAR_SEPA"  # parallel and separate
    elif is_two_planes_intersect(matA, matB) == "PLANES_COPLANAR":
        polygonB = get_discrete_points_from_section(secB)
        for point in polygonB:
            if is_point_in_polygon(point, polygonA):
                return "COPLANAR_INTER"
        return "COPLANAR_SEPA"
    else:  # two sections intersect
        for iter in fragsB:
            if isinstance(iter, Segment):
                if is_line_locate_on_plane(iter, secA.transformation, False) == "LINE_INTER":
                    point = get_intersect_point_of_line_plane(
                        iter, secA.transformation)[0]
                    if is_point_in_polygon(point, polygonA):
                        return "NOT_COPLANAR_INTER"
            elif isinstance(iter, Arc):
                if is_arc_locate_on_plane(iter, secA.transformation) == "ARC_INTERSECT":
                    points = get_intersect_point_of_arc_plane(
                        iter, secA.transformation)
                    for point in points:
                        if is_point_in_polygon(point, polygonA):
                            return "NOT_COPLANAR_INTER"
            elif isinstance(iter, SplineCurve):
                spoints = get_discrete_points_from_spline(iter)
                for point in spoints:
                    if is_point_in_polygon(point, polygonA):
                        return "NOT_COPLANAR_INTER"
            else:
                continue
        # double traversal
        for iter in fragsA:
            if isinstance(iter, Segment):
                if is_line_locate_on_plane(iter, secB.transformation, False) == "LINE_INTER":
                    point = get_intersect_point_of_line_plane(
                        iter, secB.transformation)[0]
                    if is_point_in_polygon(point, polygonB):
                        return "NOT_COPLANAR_INTER"
            elif isinstance(iter, Arc):
                if is_arc_locate_on_plane(iter, secB.transformation) == "ARC_INTERSECT":
                    points = get_intersect_point_of_arc_plane(
                        iter, secB.transformation)
                    for point in points:
                        if is_point_in_polygon(point, polygonB):
                            return "NOT_COPLANAR_INTER"
            elif isinstance(iter, SplineCurve):
                spoints = get_discrete_points_from_spline(iter)
                for point in spoints:
                    if is_point_in_polygon(point, polygonB):
                        return "NOT_COPLANAR_INTER"
            else:
                continue
        return "NOT_COPLANAR_SEPA"


# ------------------------------------------------------------------------------------------
# |                                      DIMENSION                                         |
# ------------------------------------------------------------------------------------------


# 判断Line是否闭合
def is_line_close(line: Line) -> bool:
    parts = get_nested_parts_from_line(line)
    if len(parts) >= 1:
        pointStart = get_part_start_point(parts[0])
        pointEnd = get_part_end_point(parts[-1])
        if is_coincident(pointEnd, pointStart):
            return True
    return False


# 判断Line在XoY二维平面
def is_line_in_two_dimensional(param) -> bool:
    if isinstance(param, (GeVec2d, GeVec3d)):
        return is_float_zero(to_vec3(param).z)
    elif isinstance(param, (list, tuple)):  # len(param)==2: #segment
        for iter in param:
            if not is_line_in_two_dimensional(iter):
                return False
        return True
    elif isinstance(param, Segment):
        return is_float_zero(abs(to_vec3(param.start).z)+abs(to_vec3(param.end).z))
    elif isinstance(param, Arc):
        return is_two_dimensional_matrix(param.transformation)
    elif isinstance(param, SplineCurve):
        for point in param.points:
            if not is_float_zero((param.transformation*point).z):
                return False
        return True
    elif isinstance(param, Line):
        parts = get_nested_parts_from_line(param)
        for part in parts:
            if not is_line_in_two_dimensional(part):  # recursion
                return False
        return True
    elif isinstance(param, Section):
        parts = get_nested_parts_from_section(param)
        for part in parts:
            if not is_line_in_two_dimensional(part):  # recursion
                return False
        return True
    else:
        raise TypeError('parameter error!')


# 参数是否全部在同一个平面上（支持多种类型）
def is_parts_locate_on_plane(param, plane: GeTransform) -> bool:
    if isinstance(param, (GeVec2d, GeVec3d)):
        return is_point_on_plane(to_vec3(param), plane)
    elif isinstance(param, (list, tuple)):  # and len(param)==2:
        # return True if(is_point_on_plane(param[0],mat) and is_point_on_plane(param[1],mat)) else False
        for iter in param:
            if not is_parts_locate_on_plane(iter, plane):
                return False
        return True
    elif isinstance(param, Arc):
        return is_two_planes_intersect(param.transformation, plane) == "PLANES_COPLANAR"
    elif isinstance(param, SplineCurve):
        for point in param.points:
            if not is_point_on_plane(param.transformation*point, plane):
                return False
        return True
    elif isinstance(param, Line):
        parts = get_nested_parts_from_line(param)
        for part in parts:
            if not is_parts_locate_on_plane(part, plane):  # recursion
                return False
        return True
    elif isinstance(param, Section):
        parts = get_nested_parts_from_section(param)
        for part in parts:
            if not is_parts_locate_on_plane(part, plane):  # recursion
                return False
        return True
    else:
        raise TypeError('Line parameter error!')


# 线（参数）共面
def is_line_on_same_plane(line: Line) -> bool:
    mat = get_first_matrix_from_line(line)
    parts = get_nested_parts_from_line(line)
    for part in parts:
        if (not is_parts_locate_on_plane(part, mat)):
            return False
    return True


# 获取Line的类型
def get_line_dimensional_type(line: Line) -> str:
    '''
    # LINE_3D, //参数为vec3，且不在同一平面
    # LINE_XOY, //参数位于XoY平面(vec3)
    # LINE_SECTION, //参数位于同一平面（可能在3维空间）
    '''
    # if (is_two_dimensional_matrix(line.m_transformation) and is_all_vec2(line.m_parts)):
    #     return "LINE_2D"
    if (not is_line_on_same_plane(line)):
        return "LINE_3D"
    return "LINE_XOY" if(is_line_in_two_dimensional(line)) else "LINE_SECTION"


# ------------------------------------------------------------------------------------------
# |                                      CALCULATE                                         |
# ------------------------------------------------------------------------------------------


# 二维圆弧的包围盒
def get_range_of_arc_2D(arc: Arc, returnPoints=False) -> list:
    # calculate range of arc on XoY plane.
    mat = arc.transformation
    if (not is_two_dimensional_matrix(arc.transformation)) and \
       (not is_shadow_matrix_on_xoy(arc.transformation)):
        raise TypeError('arc must locate on XoY!')
    a, b, thetaL, thetaR = get_arc_rotate_angle_2D(arc, True)
    # create_geometry(rotz(thetaL)*scale(a, b)*rotz(thetaR)*Arc())
    pos = get_matrixs_position(mat)
    pRelaS = arc.pointStart-pos
    pRelaE = arc.pointEnd-pos
    if is_float_zero(thetaL):
        xR = abs(a)
        yT = abs(b)
        px = GeVec3d(xR, 0)
        py = GeVec3d(0, yT)
    else:  # the unique solution calculate
        if thetaL > 0:
            k1 = -tan(thetaL)  # y
            k2 = -1/k1
            c1 = sqrt(a**2*k1**2+b**2)  # yTop
            x1 = (-a**2*k1*c1)/(a**2*k1**2+b**2)
            y1 = k1*x1+c1
            c2 = -sqrt(a**2*k2**2+b**2)  # -> xRight
            x2 = (-a**2*k2*c2)/(a**2*k2**2+b**2)
            y2 = k2*x2+c2
            py = rotz(thetaL)*GeVec3d(x1, y1)  # yMax
            px = rotz(thetaL)*GeVec3d(x2, y2)  # xMax
        else:
            k1 = 1/tan(thetaL)  # x
            k2 = -1/k1
            c1 = sqrt(a**2*k1**2+b**2)  # xRight
            x1 = (-a**2*k1*c1)/(a**2*k1**2+b**2)
            y1 = k1*x1+c1
            c2 = sqrt(a**2*k2**2+b**2)  # -> yTop
            x2 = (-a**2*k2*c2)/(a**2*k2**2+b**2)
            y2 = k2*x2+c2
            px = rotz(thetaL)*GeVec3d(x1, y1)  # xMax
            py = rotz(thetaL)*GeVec3d(x2, y2)  # yMax
    arc = trans((-1.0)*pos)*arc  # transfer arc center to origin point.
    if is_point_on_arc(px, arc, True) == 'POINT_ON' or \
            is_point_on_arc(px, arc, True) == 'POINT_END':
        xMax = px.x
        pxMax = GeVec2d(xMax, 0)
    else:
        xMax = max(pRelaS.x, pRelaE.x)
        pxMax = arc.pointStart if (pRelaS.x > pRelaE.x) else arc.pointEnd
    if is_point_on_arc((-1.0)*px, arc, True) == 'POINT_ON' or \
            is_point_on_arc((-1.0)*px, arc, True) == 'POINT_END':
        xMin = -(px.x)
        pxMin = GeVec2d(xMin, 0)
    else:
        xMin = min(pRelaS.x, pRelaE.x)
        pxMin = arc.pointStart if (pRelaS.x < pRelaE.x) else arc.pointEnd
    if is_point_on_arc(py, arc, True) == 'POINT_ON' or \
            is_point_on_arc(py, arc, True) == 'POINT_END':
        yMax = py.y
        pyMax = GeVec2d(0, yMax)
    else:
        yMax = max(pRelaS.y, pRelaE.y)
        pyMax = arc.pointStart if (pRelaS.y > pRelaE.y) else arc.pointEnd
    if is_point_on_arc((-1.0)*py, arc, True) == 'POINT_ON' or \
            is_point_on_arc((-1.0)*py, arc, True) == 'POINT_END':
        yMin = -(py.y)
        pyMin = GeVec2d(0, yMin)
    else:
        yMin = min(pRelaS.y, pRelaE.y)
        pyMin = arc.pointStart if (pRelaS.y < pRelaE.y) else arc.pointEnd
    if returnPoints:  # origin point relative to world-coord
        return (xMin+pos.x, xMax+pos.x, yMin+pos.y, yMax+pos.y,
                pxMin+pos, pxMax+pos, pyMin+pos, pyMax+pos)
    else:
        return (xMin+pos.x, xMax+pos.x, yMin+pos.y, yMax+pos.y)


# 二维平面包围盒范围（仅点和圆弧）
def get_range_of_section_2D(sec: Section, returnPoints=False) -> list:
    parts = get_nested_parts_from_section(sec)  # already vec3
    p = get_first_point_on_section(sec)
    # point with z value
    xMin = xMax = p.x
    yMin = yMax = p.y
    pxMin = pxMax = p
    pyMin = pyMax = p
    for iter in parts:
        if isinstance(iter, GeVec3d):
            if iter.x < xMin:
                xMin = iter.x
                pxMin = iter
            if iter.x > xMax:
                xMax = iter.x
                pxMax = iter
            if iter.y < yMin:
                yMin = iter.y
                pyMin = iter
            if iter.y > yMax:
                yMax = iter.y
                pyMax = iter
        elif isinstance(iter, Arc):
            res = get_range_of_arc_2D(iter, True)
            if res[0] < xMin:
                xMin = res[0]
                pxMin = res[4]
            if res[1] > xMax:
                xMax = res[1]
                pxMax = res[5]
            if res[2] < yMin:
                yMin = res[2]
                pyMin = res[6]
            if res[3] > yMax:
                yMax = res[3]
                pyMax = res[7]
    if returnPoints:
        return (xMin, xMax, yMin, yMax, to_vec2(pxMin), to_vec2(pxMax), to_vec2(pyMin), to_vec2(pyMax))
    else:
        return (xMin, xMax, yMin, yMax)
