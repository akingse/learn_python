# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 功能函数
# Author: akingse
# Date: 2021/12

from copy import deepcopy
from .pyp3d_api import *
# import winsound

# ------------------------------------------------------------------------------------------
# |                                          ARC                                           |
# ------------------------------------------------------------------------------------------

# 3点画圆


def arc_of_three_points(*args) -> Arc:
    # args:list, isFull=False
    if len(args) == 1 and is_all_vec(args[0]):
        points = list(args[0])
        isFull = False
    elif len(args) == 2 and is_all_vec(args[0]) and isinstance(args[1], bool):
        points = list(args[0])
        isFull = args[1]
    elif len(args) == 3 and is_all_vec(args):
        points = list(args)
        isFull = False
    elif len(args) == 4 and is_all_vec([args[0], args[1], args[2]]) and isinstance(args[3], bool):
        points = [args[0], args[1], args[2]]
        isFull = args[3]
    else:
        raise ValueError('arc_of_three_points parameters error!')
    # generate arc
    # if 3 points collinear, defualt on XoY plane.
    if norm(points[2]-points[0]) < PL_A and norm(points[1]-points[0]) > PL_A:
        R = norm(points[1]-points[0])/2
        mat = trans(0.5*(points[0]+points[1]))*scale(R)
        return mat*Arc()
    else:
        mat = get_arc_from_three_points(points)[0]
        scope = 2 * pi if isFull else get_arc_from_three_points(points)[1]
        return mat*Arc(scope)


# 圆心-起点-终点
def arc_of_center_points(centerP: GeVec3d, startP: GeVec3d, endP: GeVec3d, isCcw=True) -> Arc:
    R1 = norm(startP-centerP)
    R2 = norm(endP-centerP)
    if abs(R1-R2) > PL_A or is_float_zero(R1):
        raise TypeError('not a circle arc!')
    if norm(startP-endP) < PL_A:
        return trans(centerP)*scale(R1)*Arc()  # return a full arc that ccw.
    # if 3 points collinear, defualt on XoY plane.
    if is_two_vectors_same_direction(centerP-startP, centerP-endP) == "DIRECTION_OPPO":
        # if is_all_vec2([centerP, startP, endP]):
        vecStart = startP-centerP
        mat = trans(centerP)*scale(R1)*rotz(atan2(vecStart.y, vecStart.x))
        return mat*Arc((2*int(isCcw)-1)*pi)
        # raise TypeError('cant judge arc locate plane!')
    forwM = get_matrix_from_three_points(
        [centerP, startP, endP], False)  # transfer 3D to 2D
    startR = inverse_orth(forwM)*startP
    endR = inverse_orth(forwM)*endP
    scope = get_angle_of_two_vectors(startR, endR, True)  # always posi-angle
    if isCcw:
        return forwM*scale(R1)*Arc(scope)
    else:
        return forwM*scale(R1)*Arc(scope-2*pi)


# 起点-终点-半径-定位平面
def arc_of_radius_points_3D(pStart: GeVec3d, pEnd: GeVec3d, R: float, plane=GeTransform()) -> Arc:
    pStart = inverse_orth(plane)*pStart
    pEnd = inverse_orth(plane)*pEnd
    arc = arc_of_radius_points_2D(to_vec2(pStart), to_vec2(pEnd), R)
    return plane*arc


# 起点-终点-半径
def arc_of_radius_points_2D(pStart: GeVec2d, pEnd: GeVec2d, R: float) -> Arc:
    # 仅限二维平面内
    # is_line_in_two_dimensional
    if not (isinstance(pStart, GeVec2d) and isinstance(pEnd, GeVec2d)):
        raise TypeError('parameters must in XoY plane!')
    p1 = pStart
    p2 = pEnd
    d = norm(p2-p1)
    if abs(2*R) < d:  # 2*R must greater than d
        raise TypeError('R too small !')
    thetaRela = atan2(p2.y-p1.y, p2.x-p1.x)
    thetaScope = asin(d/2/R)
    transM = trans(p1)*rotz(thetaRela)
    pCenter = transM*GeVec3d(d/2, R*cos(thetaScope), 0)
    theta = atan2(p1.y-pCenter.y, p1.x-pCenter.x)
    return trans(pCenter)*scale(abs(R))*rotz(theta)*Arc(2*thetaScope)


arc_of_radius_points = arc_of_radius_points_2D


# 三点组成线段，倒角圆弧
def arc_of_segments_bevel(points: list,  R: float) -> Arc:
    # arc_of_segments_chamfer
    if len(points) != 3:
        raise TypeError('parameters number error!')
    # while points collinear, R==0, the scale matrix is zero matrix.
    mat = get_matrix_from_three_points(points)
    pA = inverse_orth(mat)*points[0]
    pB = inverse_orth(mat)*points[1]
    pC = inverse_orth(mat)*points[2]
    angle = get_angle_of_two_vectors(pB-pA, pC-pB)
    if R <= 0:
        raise ValueError('R>0!')
    d = tan(abs(angle)/2)*R
    # ArcStart: pB-d*unitize(pB-pA), ArcEnd: pB+d*unitize(pC-pB)
    posvec = PosVec(pB-d*unitize(pB-pA), pB-pA)
    return mat*arc_of_tangent_radius_2D(posvec, math_sign(angle)*R, angle)


# 位矢-半径-角度
def arc_of_tangent_radius_2D(posVec: PosVec, R: float, scope: float) -> Arc:
    # the arc locate on XoY plane.
    # while R>0 arc center locate on left side, while scope>0 arc is anticlockwise.
    pos = posVec.pos  #
    vec = posVec.vec  # tangent direction
    if not is_line_in_two_dimensional([pos, vec]):
        raise TypeError('posVec must in XoY plane!')
    theta = atan2(vec.y, vec.x)
    # xc=pos.x-R*sin(theta)
    # yc=pos.y+R*cos(theta)
    pCenter = GeVec3d(pos.x-R*sin(theta), pos.y+R * cos(theta))
    return trans(pCenter)*scale(abs(R))*rotz(atan2(pos.y-pCenter.y, pos.x-pCenter.x))*Arc(scope)
    # temp_arc = trans(point)*rotz(pi-angle)*trans(-R, 0, 0)*scale(R)*Arc(-scope)


# 用5个点生成椭圆
def arc_of_five_points(points: list, isFull=True) -> Arc:
    # get_arc_from_five_points
    points = remove_coincident_point(points)
    forwM = get_matrix_from_points(points)
    points2D = forwM*points
    if len(points) < 5:
        raise TypeError('points parameter error!')
    # A*x=b linear system of equation
    A = []  # b=[]
    for i in range(5):
        A.append([points2D[i].x*points2D[i].y, points2D[i].y**2,
                 points2D[i].x, points2D[i].y, 1, -points2D[i].x**2])
        # b.append(-points2D[i].x**2)
    # calculate
    Ad = math_adjust_matrix(A)
    if len(Ad) < 5:
        raise TypeError('adjust matrix rank error!')
    b = [Ad[0][5], Ad[1][5], Ad[2][5], Ad[3][5], Ad[4][5]]
    x_c = math_LU_factorization(Ad, b)
    arc = get_arc_from_coefficients(x_c)  # relative arc
    if isFull:
        return forwM*arc
    else:
        a, b, thetaL, thetaR = get_arc_rotate_angle_2D(arc)
        pCenter = get_matrixs_position(arc.transformation)
        pStart = inverse_orth(trans(pCenter)*rotz(thetaL))*points2D[0]
        pEnd = inverse_orth(trans(pCenter)*rotz(thetaL))*points2D[4]
        thetaStart = atan2(pStart.y, pStart.x)
        thetaEnd = atan2(pEnd.y, pEnd.x)
        arcE = arc_of_oval_angle(a, b, thetaStart, thetaEnd, True, True)
        return forwM*trans(pCenter)*rotz(thetaL)*arcE


# 与两个圆外切的圆弧
def arc_of_two_excircles(startArc: Arc, endArc: Arc, R: float = 0,  isCcw=True) -> Arc:
    # isCcw=counter clockwise, it decide which side arc locate.
    matS = startArc.transformation
    # axisSx = get_scale_param(matS).x
    axisSx = get_matrixs_axisx(matS)
    axisSy = get_matrixs_axisy(matS)
    matE = endArc.transformation
    axisEx = get_matrixs_axisx(matE)
    axisEy = get_matrixs_axisy(matE)
    if is_two_planes_intersect(matS, matS) != "PLANES_COPLANAR":  # not coplanar
        raise TypeError('arcs not coplanear!')
    if abs(norm(axisSx)-norm(axisSy)) > PL_A or abs(norm(axisEx)-norm(axisEy)) > PL_A:
        raise TypeError('arc must be circle!')
    forwM = get_orthogonal_matrix(matS)
    centerS = GeVec2d()
    arcRela = inverse_orth(forwM)*matE
    centerE = get_matrixs_position(arcRela)
    if norm(centerS-centerE) < PL_A:
        raise TypeError('arcs center coincide!')
    C1x = centerS.x
    C1y = centerS.y
    C2x = centerE.x
    C2y = centerE.y
    R1 = norm(axisSx)
    R2 = norm(axisEx)
    if norm(centerS-centerE) > (R1+R2+2*R) and R != 0:
        raise TypeError('arcs radius error!')
    if R == 0:  # get tangent line of two arcs.
        theta = acos(abs(R1-R2)/norm(centerS-centerE))
        if not isCcw:
            theta = -theta
        pointS = get_intersect_point_of_line_arc(
            Segment(centerS, centerE), startArc)[0]
        pointE = get_intersect_point_of_line_arc(
            Segment(centerS, centerE), endArc)[0]
        pointTs = rotz(pi-theta)*pointS
        pointTe = rotate_arbitrary(centerE, g_axisZ, -theta)*pointE
        return [pointTs, pointTe]
    # the tangent arc
    if abs(centerS.y-centerE.y) < PL_A:  # horizontal line
        x = ((R1+R)**2-(R2+R)**2-(C1x*C1x-C2x*C2x) -
             (C1y*C1y-C2y*C2y))/(2*C2x-2*C1x)
        x1 = x0 = x
        y0 = sqrt((R1+R)**2-x*x)
        y1 = -y0
    elif abs(centerS.x-centerE.x) < PL_A:  # vertical line
        y = ((R1+R)**2-(R2+R)**2-(C1x*C1x-C2x*C2x) -
             (C1y*C1y-C2y*C2y))/(2*C2y-2*C1y)
        y1 = y0 = y
        x0 = sqrt((R1+R)**2-y*y)
        x1 = -x0
    else:
        A = ((2*C1x - 2*C2x)**2/(2*C1y - 2*C2y)**2 + 1)
        B = ((2*(2*C1x - 2*C2x)*((R1 + R)**2 - (R2 + R)**2 -
             (C1x*C1x-C2x*C2x)-(C1y*C1y-C2y*C2y)))/(2*C1y - 2*C2y) ** 2)
        C = ((R1 + R)**2 - (R2 + R)**2 - (C1x*C1x-C2x*C2x) -
             (C1y*C1y-C2y*C2y))**2/(2*C1y - 2*C2y)**2 - (R1 + R)**2
        x0 = math_quadratic_equation(A, B, C)[0]
        yt = sqrt((R1+R)**2-x0*x0)  # temp value
        y0 = yt if (
            abs(norm(Vec2(x0, yt))+norm(Vec2(x0, yt)-centerE)-(R1+R2+2*R)) < PL_E6) else -yt
        x1 = math_quadratic_equation(A, B, C)[1]
        yt = sqrt((R1+R)**2-x1*x1)
        y1 = yt if (
            abs(norm(Vec2(x1, yt))+norm(Vec2(x1, yt)-centerE)-(R1+R2+2*R)) < PL_E6) else -yt
    pCenter = GeVec2d(x0, y0)
    if (get_surface_of_polygon([pCenter, centerS, centerE]) > 0) ^ isCcw:  # (^==xor)
        pCenter = GeVec2d(x1, y1)
    pStart = pCenter-R*unitize(pCenter-centerS)
    pEnd = pCenter-R*unitize(pCenter-centerE)
    return forwM*arc_of_center_points(pCenter, pStart, pEnd, isCcw)


# 设定长轴短轴、起始角终止角的标准椭圆
def arc_of_oval_angle(ax=1, by=1, startAngle=0, endAngle=2*pi, isCcw=True, isAlpha=True) -> Arc:
    if isAlpha:  # isAlpha using oval point angle alpha
        startAngle = arc_alpha2theta(startAngle, ax, by)
        endAngle = arc_alpha2theta(endAngle, ax, by)
    scope = endAngle-startAngle
    if isCcw:
        scope = angle_posi(scope)
    else:
        scope = angle_nega(scope)
    arc = scale(ax, by)*rotz(startAngle)*Arc(scope)
    return arc


# 圆弧反转
def arc_reverse(arc: Arc, reCcw=True, reScope=False) -> Arc:
    # a, b, thetaL, thetaR = get_arc_rotate_angle_2D(arc)
    if not arc.isCircle:  # current nonsupport oval
        return g_matrixO*Arc()
    if reCcw and (not reScope):
        pStart, pMiddle, pEnd = get_three_points_from_arc(arc)
        return arc_of_three_points(pEnd, pMiddle, pStart)
    elif (not reCcw) and reScope:
        arcN = deepcopy(arc)
        if arcN.scope >= 0:
            arcN.scope = angle_nega(arcN.scope)
        else:
            arcN.scope = angle_posi(arcN.scope)
        return arcN
    elif reCcw and reScope:
        return arc_reverse(arc_reverse(arc, True, False), False, True)
    else:
        return arc


# 通过线段打断Arc(only circle)
def arc_of_segment_interrupt(segm: Segment, arc: Arc, cutStart=True) -> Arc:
    # segment direction: from arc.pointCenter to arc.pointStart/pointEnd
    if is_point_on_line(arc.pointStart, segm) or is_point_on_line(arc.pointEnd, segm):
        return arc
    R = norm(get_matrixs_axisx(arc.transformation))
    if segm.norm < R:  # auto inner
        segm = Segment(arc.pointCenter, segm.end+R*segm.vectorU)
    points = get_intersect_point_of_line_arc(segm, arc)
    if len(points) != 1:
        print('arc_of_segment_interrupt, no intersect point!')
        return arc
    forwM = get_orthogonal_matrix(arc.transformation)
    arcR = inverse_orth(forwM)*arc
    pointR = inverse_orth(forwM)*points[0]
    if cutStart:
        angle = get_angle_of_two_vectors(arcR.pointStart, pointR)
        arcN = arc.transformation*rotz(angle) * Arc(arc.scope-angle)
        return arcN
    else:
        angle = get_angle_of_two_vectors(arcR.pointEnd, pointR)
        arcN = deepcopy(arc)
        arcN.scope = arc.scope+angle
        return arcN


# ------------------------------------------------------------------------------------------
# |                                       PATTERN                                          |
# ------------------------------------------------------------------------------------------


def five_points_star(R: float = 100, isClose=False) -> list:  # 十点五角星(外接圆半径)
    # R is the radius of circum-circle
    a = 1
    b = a/tan(18*pi/180)
    d = a*tan(54*pi/180)
    c = a/sin(18*pi/180)
    r = sqrt((a+c)**2+d**2)
    p1 = GeVec2d(a, d)
    p2 = GeVec2d(0, b+d)
    points = [p1, p2]
    for i in range(1, 5):
        points.append(rotz(i*72*pi/180)*p1)
        points.append(rotz(i*72*pi/180)*p2)
    if isClose:
        points.append(p1)
    # return scale(R/r)*Section(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p0)
    return scale(R/r)*points


def regular_polygon(num: int, length: float, isR=True) -> list:  # XoY平面正多边形
    # 边数-边长/外接圆半径
    if num < 3 or length <= 0:
        raise TypeError('parameters error!')
    if not isR:  # is length or radius
        length = (length/2)/sin(pi/num)
    p1 = Vec3(length, 0, 0)
    pList = []
    for i in range(num+1):
        pList.append(rotz(i/num*2*pi)*p1)
    return pList  # closed


def rectangle_central_symmetry(x: float, y: float, R=0.0) -> list:  # 中心对称圆角矩形(XoY)
    x = abs(copy.deepcopy(x))
    y = abs(copy.deepcopy(y))
    if is_float_zero(R):
        return [GeVec2d(x, y), GeVec2d(-x, y), GeVec2d(-x, -y), GeVec2d(x, -y)]
    else:
        return rectangle_diagonal(GeVec2d(-x, -y), GeVec2d(x, y), R).parts


def rectangle_diagonal(pointA: GeVec2d, pointC: GeVec2d, R=0.0) -> Section:  # 对角线圆角矩形(XoY)
    # rectangle rounded 自动生成带有倒角的对角线矩形section，与坐标系轴平行(pointA左下->pointC右上)
    if not is_line_in_two_dimensional([pointA, pointC]):
        raise ValueError('points must in two dimensional!')
    p1 = to_vec2(copy.deepcopy(pointA))
    p2 = to_vec2(copy.deepcopy(pointC))
    if (p1-p2).x >= 0 and (p1-p2).y >= 0:
        p1, p2 = p2, p1  # swap value
    q1 = GeVec2d(p2.x, p1.y)
    q2 = GeVec2d(p1.x, p2.y)
    if abs(R) < PL_A:  # without arc chamfer
        return Section(p1, q1, p2, q2)
    if abs(p1.x-p2.x) < PL_A or abs(p1.y-p2.y) < PL_A:  # collinear become segment
        return Section(p1, q1, p2, q2)
    d = min(abs(p2.x-p1.x), abs(p2.y-p1.y))
    if R < 0 or R > d/2:
        raise ValueError('R value error!')
    else:
        dx = math_sign(p2.x-p1.x)*GeVec2d(R, 0)
        dy = math_sign(p2.y-p1.y)*GeVec2d(0, R)
        return Section(trans(q1-dx+dy)*rotz(-pi/2)*scale(R)*Arc(pi/2),
                       trans(p2-dx-dy)*rotz(0)*scale(R)*Arc(pi/2),
                       trans(q2+dx-dy)*rotz(pi/2)*scale(R)*Arc(pi/2),
                       trans(p1+dx+dy)*rotz(pi)*scale(R)*Arc(pi/2))
        # return Section(p1+dx, q1-dx, trans(q1-dx+dy)*rotz(-pi/2)*scale(R)*Arc(pi/2),
        #                q1+dy, p2-dy, trans(p2-dx-dy) *
        #                rotz(0)*scale(R)*Arc(pi/2),
        #                p2-dx, q2+dx, trans(q2+dx-dy) *
        #                rotz(pi/2)*scale(R)*Arc(pi/2),
        #                q2-dy, p1+dy, trans(p1+dx+dy)*rotz(pi)*scale(R)*Arc(pi/2))


# ------------------------------------------------------------------------------------------
# |                                        BODY                                            |
# ------------------------------------------------------------------------------------------


def sweep_mubiu_arc(sec: Section, R: float, times: int = 1, disNum=0) -> Loft:  # 莫比乌斯环(圆环)
    # 截面，圆环半径，旋转圈数
    secM = rotx(pi/2)*sec
    if disNum == 0:
        disNum = 100*times
    secList = []
    for i in range(int(disNum)+1):
        secList.append(rotz(i/disNum*2*pi)*trans(R, 0)
                       * roty(i/disNum*times*2*pi)*secM)
    geo = Loft(secList)
    geo.smooth = True
    return geo


def std_tetrahedron(t: float = 100) -> Loft:  # 正四面体 pyramid shape
    sectionA = Section(Vec2(0, 0), Vec2(2, 0), Vec2(1, sqrt(3)))
    sectionB = rotx(atan(3))*sectionA
    geo = scale(t)*trans(-1, -1/sqrt(3))*Loft(sectionA, sectionB)
    return geo


def std_ring(rOut: float, rSec: float, scope: float = 2*pi) -> Sweep:  # 圆环
    return Sweep(rotx(pi/2)*Section(trans(rOut, 0)*scale(rSec)*Arc()), Line(Arc(scope)))


def conus_diameter_height(d: float, h: float) -> Loft:  # （标准）圆锥
    arcBottom = Section(scale(0.5*d)*Arc())
    arcTop = trans(0, 0, h)*Section(scale(PL_E6)*Arc())
    return Loft(arcBottom, arcTop)
    # sec=rotx(pi/2)*Section(GeVec2d(0,0),GeVec2d(0.5*d,0),GeVec2d(0,h)) #another method
    # return Sweep(sec,Line(Arc()))


def conus_underside_vertex(arc: Arc, pVertex: GeVec3d) -> Loft:  # （顶点）圆锥
    pCenter = arc.pointCenter
    arcBottom = Section(arc)
    arcT = deepcopy(arc)
    arcT.scale_center(PL_E6)
    arcTop = trans(pVertex-pCenter)*Section(arcT)
    return Loft(arcBottom, arcTop)

# ------------------------------------------------------------------------------------------
# |                                        SHOW                                            |
# ------------------------------------------------------------------------------------------


def show_extend_line(line: Segment, showPoints=False) -> Combine:  # 显示线段所在直线（延长线）
    limit = 1e5
    p = to_vec3(line.start)
    q = to_vec3(line.end)
    if norm(p) > limit or norm(q) > limit or norm(p-q) < PL_A:
        return
    k = 10
    kx = abs((p+k*(q-p)).x)
    ky = abs((p+k*(q-p)).y)
    kz = abs((p+k*(q-p)).z)
    if kx >= ky and kx >= kz:
        k = (limit-p.x)/(q-p).x
    elif ky >= kx and ky >= kz:
        k = (limit-p.y)/(q-p).y
    else:  # elif kx>=ky and kx>=kz:
        k = (limit-p.z)/(q-p).z
    geo = Combine(Line(p+k*(q-p), p-k*(q-p)).color(0.5, 0.2, 1))
    if showPoints:
        geo.append(trans(p)*Sphere())
        geo.append(trans(q)*Sphere())
    create_geometry(geo)
    return geo


def show_coordinate_plane(mat: GeTransform = g_matrixE, sca=1) -> Combine:  # 显示坐标系及XoY平面
    mat = get_orthogonal_matrix(mat)
    geo = Combine(show_coordinate_system(mat, sca, 1))
    geo.append(mat*scale(100*sca)*Section(Vec2(0, 0), Vec2(2, 0),
               Vec2(2, 1), Vec2(0, 1)).color(1, 1, 0, 0.5))
    create_geometry(geo)
    return geo


def show_line_extend(p, isX=True):
    k = 1e5  # max=1e16
    if isX:
        if isinstance(p, (int, float)):
            x = p
        elif isinstance(p, (GeVec2d, GeVec3d)):
            x = p.x
        create_geometry(Line(Vec2(x, -k), Vec2(x, k)).colorGreen())
    else:
        if isinstance(p, (int, float)):
            y = p
        elif isinstance(p, (GeVec2d, GeVec3d)):
            y = p.y
        create_geometry(Line(Vec2(-k, y), Vec2(k, y)).colorRed())


def show_section_box_surround_2D(sec):
    res = get_range_of_section_2D(sec)
    show_line_extend(res[0], True)
    show_line_extend(res[1], True)
    show_line_extend(res[2], False)
    show_line_extend(res[3], False)


def show_coordinate_system(mat: GeTransform = g_matrixE, scal=1, kr=1) -> Combine:  # 显示坐标系
    '''
    0<=k<=10: proportion coefficient, adjust the of proportion coordinate_system axis;
    s: scale coefficient, while s=1 base length is 100;
    '''
    l = 10  # base length
    if kr < 0:  # the scale of radius
        kr = 1
    elif kr > 10:
        kr = 10
    R = 1.5*(kr*2)
    sylinder = trans(0, 0, sqrt(5)/3*R)*Sweep(Section(scale(kr*2)
                                                      * (Arc())), Line(Vec3(), Vec3(0, 0, 7*l-sqrt(5)/3*R)))
    conus = trans(0, 0, 7*l)*conus_diameter_height(3*kr*2, 3*l)
    axis = Combine(sylinder, conus)
    axisO = scale(R)*Sphere().color(0.2, 0.2, 0.2)
    axisZ = rotz(0)*axis.color(0, 0, 1)
    axisY = rotx(-pi/2)*axis.color(0, 1, 0)
    axisX = roty(pi/2)*axis.color(1, 0, 0)
    geo = mat*scale(scal)*Combine(axisO, axisX, axisY, axisZ)
    create_geometry(geo)
    return geo


def show_points_line(points: list, radius=0, withEnd=True, isShow=True) -> Combine:  # 显示点线
    # make coincident point swell
    # points = remove_coincident_point(to_vec3(points))
    points = to_vec3(points)
    geo = Combine()
    if len(points) == 0:
        return geo
    if len(points) == 1:
        if radius == 0:
            radius = 10  # norm(points[0])
        geo = trans(points[0])*scale(radius)*Sphere().colorMagenta()
        create_geometry(geo)
        return geo
    lenList = [100]
    for i in range(len(points)-1):
        if norm(points[i]-points[i+1]) > PL_A:  # only add non-zero norm vector
            lenList.append(norm(points[i]-points[i+1]))
    if norm(points[0]-points[-1]) > PL_A:
        lenList.append(norm(points[0]-points[-1]))
    minR = min(lenList)
    if radius == 0:
        radius = minR/25
    elif radius > minR/4:
        radius = minR/4
    # using next point, compare to previous point
    geo.append(trans(points[0])*scale(radius) * Sphere().colorMagenta())
    for i in range(1, len(points)):
        if norm(points[i]-points[i-1]) < PL_A:
            geo.append(trans(points[i])*scale(2*radius)
                       * Sphere().colorMagenta())
        else:
            # unitize the direciton vector.
            vec = unitize(points[i]-points[i-1])
            geo.append(Cone(points[i-1]+(sqrt(3)/2*radius)*vec, points[i] -
                            (3*radius)*vec, radius/2, radius/2).colorOrange())  # the cyclinder of line.
            mat = get_matrix_from_two_points(
                points[i]-(3*radius)*vec, points[i])
            # the Conus arrow of direction.
            geo.append(mat*conus_diameter_height(1.5 *
                                                 radius, 2*radius).colorCyan())
            if withEnd or i != len(points)-1:
                geo.append(trans(points[i])*scale(radius)
                           * Sphere().colorMagenta())  # the center sphere.
    if isShow:
        create_geometry(geo)
    return geo


def show_standard_height_plane(high=0, text="", sca=1) -> Section:  # 标高参考平面
    point = scale(sca)*GeVec3d(1e3, 1e3, high)
    sec = Section(point, rotz(pi/2)*point, rotz(pi)*point,
                  rotz(-pi/2)*point).color(0.5, 0.5, 0.5, 0)
    text = text+" h="+str(high)
    tex = Text(text).color(0.5, 0.5, 0.5, 0)
    tex.size = 100*sca
    geo = Combine(sec, trans(scale(sca)*GeVec3d(-1e3, -1e3, high))*tex)
    create_geometry(geo)
    return geo


# ------------------------------------------------------------------------------------------
# |                                        CURVE                                           |
# ------------------------------------------------------------------------------------------


def std_oval(t) -> GeVec3d:  # 椭圆
    a = 300
    b = 200
    return GeVec3d(a*cos(t), b*sin(t), 0)


def std_hyperbola(t) -> GeVec3d:  # 双曲线
    a = 1
    b = 1
    return GeVec3d(a*1/cos(t), b*tan(t), 0)


def std_parabola(t) -> GeVec3d:  # 抛物线
    c = 1
    a = 0.3
    return GeVec3d(2*c*t, a*t*t, 0)


def std_spiral_line_out(t, k=0.1) -> GeVec3d:  # 螺旋线out
    return GeVec3d(t*cos(k*t), t*sin(k*t), 0)


def std_spiral_line_up(t, c=100) -> GeVec3d:  # 螺旋线up
    return GeVec3d(c*cos(t/10), c*sin(t/10), t)


def std_cycloid(t, r=1) -> GeVec3d:  # 摆线
    x = r*(t-sin(t))
    y = r*(1-cos(t))
    return GeVec3d(x, y, 0)


def std_sine(t, A=1, phi=0) -> GeVec3d:  # sin函数
    return GeVec3d(t, A*sin(t+phi), 0)


def std_involute(R: float, phi):  # 渐开线(for gear)
    return GeVec3d(R*(cos(phi)+phi*sin(phi)), R*(sin(phi)+phi*cos(phi)))


# ------------------------------------------------------------------------------------------
# |                                        PRINT                                           |
# ------------------------------------------------------------------------------------------


def print_matrix(mat: GeTransform, info: str = "the GeTransform matrix") -> None:  # print 3x4 矩阵，测试专用
    m = appro_matrix(mat)
    print('|'+info.center(90, '-')+'|')
    print([m._mat[0][0], m._mat[0][1], m._mat[0][2], m._mat[0][3]])
    print([m._mat[1][0], m._mat[1][1], m._mat[1][2], m._mat[1][3]])
    print([m._mat[2][0], m._mat[2][1], m._mat[2][2], m._mat[2][3]])
    print('|'+90*"_"+"|\n")


def print_vector(*args) -> None:
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    else:
        args = list(args)
    for point in args:
        pnt = to_vec3(point)
        pnt = Vec3(appro_num(pnt.x), appro_num(pnt.y), appro_num(pnt.z))
        print(pnt)


def print_result(res: bool) -> None:
    print("test pass") if (res) else print("test error!!!!!!!!!!!!!!!!!!!!")
    # if not res:
    #     winsound.Beep(800, 1000)


# to wangqingwei
def get_nearest_distance_of_two_segment(seg1: Segment, seg2: Segment) -> float:
    # the nearest_point of segment1 start to segment2
    dn1 = get_nearest_point_of_point_line(seg1.start, seg2)
    if is_point_on_segment(dn1, seg2, False) == "POINT_END" or \
            is_point_on_segment(dn1, seg2, False) == "POINT_IN":
        dmin1 = norm(seg1.start-dn1)
    else:
        dmin1 = min(norm(seg1.start-seg2.start), norm(seg1.start-seg2.end))
    # the nearest_point of segment1 end to segment2
    dn2 = get_nearest_point_of_point_line(seg1.end, seg2)
    if is_point_on_segment(dn2, seg2, False) == "POINT_END" or \
            is_point_on_segment(dn2, seg2, False) == "POINT_IN":
        dmin2 = norm(seg1.end-dn1)
    else:
        dmin2 = min(norm(seg1.end-seg2.start), norm(seg1.end-seg2.end))
    return min(dmin1, dmin2)


def arc_of_angle_and_radius_2D(angle, R, scope) -> Arc:
    return scale(R)*Arc(scope)
