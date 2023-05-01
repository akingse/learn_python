# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# Author: akingse
# Date: 2021/10

from .pyp3d_transfer import *


# ------------------------------------------------------------------------------------------
# |                                      PERIMETER                                         |
# ------------------------------------------------------------------------------------------


def get_perimeter_of_polygon(line: list, close=False) -> float:  # 多段线周长
    length = 0.0
    if len(line) == 0:
        return length
    for i in range(len(line)-1):
        length += norm(line[i+1]-line[i])
    if close:
        length += norm(line[-1]-line[0])
    return length


def get_perimeter_of_arc(oval: Arc) -> float:  # 椭圆周长(近似值)
    def _perimeter(th):  # second integration formula of arc.
        # return sqrt((a*cos(th)) ** 2+(b*sin(th)) ** 2)
        return a*sqrt(1-e*e*cos(th)*cos(th))
    forwM = get_orthogonal_matrix(oval.transformation)
    if is_two_dimensional_matrix(forwM):  # is2D=True
        forwM = g_matrixE
    arc = inverse_orth(forwM)*oval
    if arc.isCircle:
        return abs(oval.scope*norm(get_matrixs_axisx(oval.transformation)))
    else:
        a, b, thetaL, thetaR = get_arc_rotate_angle_2D(arc)
        e = sqrt(1-(b*b)/(a*a))
        # get the circle central angle
        thetaEnd = thetaR+oval.scope  # the oval scope is circle central angle.
        if arc.isFull:  # switch perimeter formula
            lamda = (a-b)/(a+b)
            # Ramanujan approximate formula
            perim = pi*(a+b)*(1+(3*lamda**2)/(10+sqrt(4-3*lamda**2)))
            return abs(oval.scope/(2*pi)*perim)
        else:
            perim = 0.0
            disNum = 3600
            stepT = (thetaEnd-thetaR)/disNum
            for i in range(disNum):
                perim = perim+(_perimeter(thetaR+stepT*i) +
                               _perimeter(thetaR+stepT*(i+1)))*stepT/2
        return abs(perim)
    # a, b, thetaL, thetaR = get_arc_rotate_angle_2D(arc)
    # thetaEnd = thetaR+oval.scope
    # stepT = (thetaEnd-thetaR)/disNum
    # for i in range(disNum): #calculate each pair points distance
    #     di = norm(GeVec3d(a*cos(thetaR+(i+1)*stepT), b*sin(thetaR+(i+1)*stepT)) -
    #             GeVec3d(a*cos(thetaR+i*stepT), b*sin(thetaR+i*stepT)))
    #     perim += di
    # return perim


def get_perimeter_of_spline(spline: SplineCurve) -> float:  # 离散计算周长
    points = get_discrete_points_from_spline(spline)
    return get_perimeter_of_polygon(points)


def get_perimeter_of_fragment(fragm) -> float:
    if isinstance(fragm, Segment) or (isinstance(fragm, list) and len(fragm) == 2):
        return fragm.norm  # fragm[1]-fragm[0]
    elif isinstance(fragm, Arc):
        return get_perimeter_of_arc(fragm)
    elif isinstance(fragm, SplineCurve):
        return get_perimeter_of_spline(fragm)
    else:
        return 0.0


def get_perimeter_of_line(line: Line, onlyCurve=False, close=False) -> float:  # 轮廓线周长
    frags = get_fragments_from_line(line, close)
    length = 0.0
    for iter in frags:
        if isinstance(iter, Segment):
            if not onlyCurve:
                length += iter.norm
        elif isinstance(iter, Arc):
            length += get_perimeter_of_arc(iter)
        elif isinstance(iter, SplineCurve):
            length += get_perimeter_of_spline(iter)
        else:
            raise ValueError('get_perimeter_of_line nonsupport!')
    return length


def get_perimeter_of_section(sec: Section) -> float:
    return get_perimeter_of_line(sec.transformation*Line(sec.parts), onlyCurve=False, close=True)


def get_amount_of_line_segment(line: Line, close=False) -> int:
    frags = get_fragments_from_line(line, close)
    amount = 0
    for iter in frags:
        if isinstance(iter, Segment):
            amount += 1
    return amount


# ------------------------------------------------------------------------------------------
# |                                       DISCRETE                                         |
# ------------------------------------------------------------------------------------------


# 线段离散（withEnd控制是否保留末尾点）
def get_discrete_points_from_segment(segm: Segment, disNum=0, withEnd=True) -> list:
    a = segm.start
    b = segm.end
    if disNum == 0:  # the default discrete number
        length = segm.norm
        disNum = int(length/20) if int(length/20) >= 10 else 10
    if isinstance(a, GeVec3d) and isinstance(b, GeVec3d):
        pointList = []
        disNumO = disNum
        if withEnd:  # default == True
            disNumO = disNumO-1
        if disNumO == 0:
            disNumO = 1
        for i in range(disNum):
            pointList.append(a+i/disNumO*(b-a))
        return pointList
    elif isinstance(a, GeVec2d) and isinstance(b, GeVec2d):
        return to_vec2(get_discrete_points_from_segment(Segment(to_vec3(a), to_vec3(b)), disNum, withEnd))
    else:
        raise TypeError('segment discrete improper parameter!')


def get_discrete_points_from_arc(arcO: Arc, disNum=0, withEnd=True, isEqual=False) -> list:  # 圆弧离散
    def _perimeter(th):
        return a*sqrt(1-e*e*cos(th)*cos(th))
    perim = get_perimeter_of_arc(arcO)
    if disNum == 0:  # the default discrete number
        disNum = int(perim/20) if int(perim/20) >= 10 else 10
    # choose different ways to discrete
    if (not isEqual) or arcO.isCircle:
        pointList = []
        disNumO = disNum  # record the original discrete number
        if withEnd:
            disNumO = disNumO-1
        if disNumO == 0:
            disNumO = 1
        for i in range(disNum):  # i/disNum get to 1
            pointI = GeVec3d(cos(i/disNumO*arcO.scope),
                             sin(i/disNumO*arcO.scope))
            pointList.append(arcO.transformation*pointI)
        return pointList
    else:  # using second integration of arc, discrete oval equal length.
        forwM = get_orthogonal_matrix(arcO.transformation)
        if is_two_dimensional_matrix(forwM):  # is2D=True
            arcO = arcO
        else:
            arcO = inverse_orth(forwM)*arcO
        a, b, thetaL, thetaR = get_arc_rotate_angle_2D(arcO)
        if abs(a*b) < PL_A:
            return [arcO.pointCenter]*disNum  # same points of arc center
        e = sqrt(1-(b*b)/(a*a))
        disAccu = 3600
        stepA = arcO.scope/disAccu  # fixed step, circle central
        theta = thetaR  # cricle start angle.
        thetaList = [theta]
        sigma = 0  # count every step accumulative length
        if withEnd:
            disNum = disNum-1
        for i in range(1, disNum):
            while(sigma-i*perim/disNum < 0):
                sigma += abs((_perimeter(theta) +
                              _perimeter(theta+stepA)) * stepA/2)
                theta += stepA
            thetaList.append(theta-stepA)  # using fore angle
        if withEnd:
            thetaList.append(thetaR+arcO.scope)
        pointList = []
        for iter in thetaList:
            pointI = GeVec3d(a*cos(iter), b*sin(iter))
            pointList.append(pointI)
        if is_two_dimensional_matrix(forwM):
            return get_translate_matrix(arcO.transformation)*rotz(thetaL)*pointList
        else:
            return forwM*get_translate_matrix(arcO.transformation)*rotz(thetaL)*pointList


def get_discrete_points_from_spline(spline: SplineCurve, disNum=0, withEnd=True) -> list:
    # list mutiply matrix
    ctrlPoints = to_vec3(spline.points, spline.transformation)
    if disNum == 0:
        disNum = spline.num
    if not withEnd:
        disNum = disNum+1
    disPoints = spline_curve_quasi(ctrlPoints, disNum, spline.k)  # .parts
    if not withEnd:
        disPoints.pop()
    return disPoints


def get_discrete_points_from_fragment(fragm, disNum=0, withEnd=True) -> list:
    if isinstance(fragm, Segment):
        return get_discrete_points_from_segment(fragm, disNum, withEnd)
    elif isinstance(fragm, Arc):
        return get_discrete_points_from_arc(fragm, disNum, withEnd)
    elif isinstance(fragm, SplineCurve):
        return get_discrete_points_from_spline(fragm, disNum, withEnd)
    else:
        return []


# 离散化line为GeVec3d列表
def get_discrete_points_from_line(line: Line, disNumO: int = 0, onlyCurve=True, isClose=False) -> list:
    line = copy.deepcopy(line)  # deepcopy, to avoid refresh imput value
    length = get_perimeter_of_line(line, onlyCurve, isClose)
    if disNumO == 0:  # the default discrete number
        stepL = 20
        disNum = int(length/stepL) if int(length/stepL) >= 10 else 10
        disNumO = disNum
    if onlyCurve:
        parts = get_nested_parts_from_line(line)
        if is_all_vec(parts):
            return parts
        disNum = disNumO-get_amount_of_line_segment(line, isClose)-1
    else:
        disNum = disNumO-1  # last fragment without end point
    stepL = length/disNum
    fragmList = get_fragments_from_line(line, isClose)
    disPoints = []
    numSum = 0  # to keep the original discrete number
    # fragmRec=[] #
    for i in range(len(fragmList)-1):  # to control discrete number, process last fragment
        if isinstance(fragmList[i], Arc):
            numI = round(get_perimeter_of_arc(fragmList[i])/stepL)
            numSum = numSum+numI  # record total discrete number
            pointsArc = get_discrete_points_from_arc(
                fragmList[i], numI, False, False)
            disPoints += pointsArc
        elif isinstance(fragmList[i], Segment):
            if onlyCurve:
                numSum = numSum+1
                disPoints.append(fragmList[i].start)
            else:
                numI = round(fragmList[i].norm/stepL)
                numSum = numSum+numI
                pointsSeg = get_discrete_points_from_segment(
                    fragmList[i], numI, False)
                disPoints += pointsSeg
        elif isinstance(fragmList[i], SplineCurve):
            numI = round(get_perimeter_of_spline(fragmList[i])/stepL)
            numSum = numSum+numI
            pointsSpline = get_discrete_points_from_spline(
                fragmList[i], numI, False)
            disPoints += pointsSpline
        else:
            raise TypeError("get_discrete_points_from_line type error!")
    # last fragment
    numLast = (disNumO-1)-numSum
    if isinstance(fragmList[-1], Arc):
        pointsArc = get_discrete_points_from_arc(fragmList[-1], numLast, False)
        disPoints += pointsArc
    elif isinstance(fragmList[-1], Segment):
        if onlyCurve:
            disPoints.append(fragmList[-1].start)
        else:
            pointsSeg = get_discrete_points_from_segment(
                fragmList[-1], numLast, False)
            disPoints += pointsSeg
    elif isinstance(fragmList[-1], SplineCurve):
        pointsSpline = get_discrete_points_from_spline(
            fragmList[i-1], numLast, False)
        disPoints += pointsSpline
    else:
        raise TypeError("get_discrete_points_from_line type error!")
    disPoints.append(get_part_end_point(fragmList[-1]))
    return disPoints


# 获取section中的三维点（已离散）list列表
def get_discrete_points_from_section(sec: Section, num: int = 0, onlyCurve=True):
    line = sec.transformation*Line(sec.parts)
    return get_discrete_points_from_line(line, num, onlyCurve, True)


def get_range_of_section(section: Section) -> list:  # 离散法，获取截面值域(视图框)
    points = get_discrete_points_from_section(section)
    return get_range_of_polygon(points)


# ------------------------------------------------------------------------------------------
# |                                        SPLINE                                          |
# ------------------------------------------------------------------------------------------
# spline curve algorithm


def spline_quasi_node_vector(n: int, k: int) -> list:  # 准均匀B样条曲线(节点函数)
    nodeVector = [0]*(n+k+2)
    piecewise = n-k+1
    if n+1 == k:
        raise TypeError('len(controlPoint) cannot equal k!')
    if piecewise == 1:
        for i in range(n+1, n+k+2):
            nodeVector[i] = 1
    else:
        flag = 1
        while flag != piecewise:
            nodeVector[k+flag] = nodeVector[k-1+flag]+1/piecewise
            flag += 1
        for i in range(n+1, n+k+2):  # range in [a,b)
            nodeVector[i] = 1
    return nodeVector


def spline_base_function(i: int, k: int, u: float, nodeVector: list) -> float:  # B样条曲线标准迭代函数
    if k == 0:
        if u >= nodeVector[i] and u < nodeVector[i+1]:
            niku = 1
        else:
            niku = 0
    else:  # python and matlab, index is different
        if abs(nodeVector[i+k]-nodeVector[i]) < PL_A:
            coef1 = 0
        else:
            coef1 = (u-nodeVector[i])/(nodeVector[i+k]-nodeVector[i])
        if abs(nodeVector[i+k+1]-nodeVector[i+1]) < PL_A:
            coef2 = 0
        else:
            coef2 = (nodeVector[i+k+1]-u)/(nodeVector[i+k+1]-nodeVector[i+1])
        niku = coef1*spline_base_function(i, k-1, u, nodeVector) + \
            coef2*spline_base_function(i+1, k-1, u, nodeVector)
    return niku


def spline_curve_quasi(points: list, discNum: int = 0, k: int = 2) -> list:  # 样条曲线函数
    # parameters check
    if k >= len(points):
        # raise TypeError('k value error (2<=k<len(points))!')
        k = len(points)-1
    pointList = to_vec3(points)
    if discNum == 0:
        length = 0
        for i in range(1, len(pointList)):
            length = norm(pointList[i]-pointList[i-1])+length
        discNum = int(length/10) if int(length/10) >= 10 else 10
    discNum = discNum-1  # ensure the discrete number
    if discNum <= len(points):
        discNum = len(points)+2
        # raise TypeError('points must more than discNum!')
    n = len(pointList)-1
    points3D = []
    P = [[], [], []]  # the control points in matrix container
    for i in range(n+1):
        P[0].append(pointList[i].x)
        P[1].append(pointList[i].y)
        P[2].append(pointList[i].z)
    Ni_k = [0]*(n+1)
    # using quasi spline method
    node = spline_quasi_node_vector(n, k)
    for u in linspace(0, 1-1/discNum, discNum):
        for i in range(n+1):
            Ni_k[i] = spline_base_function(i, int(k), u, node)
        x, y, z = 0, 0, 0
        for j in range(n+1):
            x += P[0][j]*Ni_k[j]
            y += P[1][j]*Ni_k[j]
            z += P[2][j]*Ni_k[j]
        points3D.append(GeVec3d(x, y, z))
    points3D.append(pointList[-1])
    # return Line(points3D)
    return points3D


# ------------------------------------------------------------------------------------------
# |                                         ORAL                                           |
# ------------------------------------------------------------------------------------------


def get_arc_from_coefficients(coefficients: list) -> Arc:  # XoY面椭圆一般方程互转
    # genetal formula: x^2+a*x*y+b*y^2+c*x+d*y+e==0
    # (x+k)^2+a*(x+k)*y+b*y^2+c*(x+k)+d*y+e==0
    a0, b0, c0, d0, e0 = coefficients
    k = 0  # x direciton offset param
    if abs(e0) < PL_A:
        if abs(1+c0) < PL_A:
            k = -1.0  # trans(-1,0,0)
        else:
            k = 1.0  # trans(1,0,0)
        e0 = k*(k+c0)
        c0 = c0+2*k
        d0 = d0+a0*k
    a = 1/e0  # two kinds of genetal formula.
    b = a0/e0
    c = b0/e0
    d = c0/e0
    e = d0/e0
    if(4*a*c-b*b) < PL_A or abs(a)+abs(b) < PL_A:
        raise TypeError('parameters error!')
    # transfer to genetal formula:  a*x**2+b*x*y+c*y**2+d*x+e*y+1==0
    theta = atan2(b, a-c)/2
    Xc = (b*e-2*c*d)/(4*a*c-b*b)
    Yc = (b*d-2*a*e)/(4*a*c-b*b)
    al = sqrt((2*(a*Xc**2+c*Yc**2+b*Xc*Yc-1)) /
              (a+c+sqrt((a-c)**2+b**2)))  # vertify
    bl = sqrt((2*(a*Xc**2+c*Yc**2+b*Xc*Yc-1))/(a+c-sqrt((a-c)**2+b**2)))
    return trans(Xc+k, Yc)*rotz(theta)*scale(al, bl)*Arc()


def get_coefficients_from_arc(arc: Arc) -> list:
    # genetal formula: x^2+a*x*y+b*y^2+c*x+d*y+e=0
    if not is_two_dimensional_matrix(arc.transformation):
        raise TypeError('arc must locate on XoY!')
    # the transform of relation system to world system.
    # X=(x-c)*cos(theta)-(y-d)*sin(theta)
    # Y=(y-d)*cos(theta)+(x-c)*sin(theta)
    # X^2/a^2+Y^2/b^2=1
    a, b, thetaL, thetaR = get_arc_rotate_angle_2D(arc)
    p = get_matrixs_position(arc.transformation)
    c = p.x
    d = p.y
    # reverse rotate
    # theta = -get_angle_of_two_vectors(g_axisX, get_matrixs_axisx(mat))
    co = cos(thetaL)
    sn = sin(thetaL)
    a0 = b*b*co*co+a*a*sn*sn
    b0 = (2*a*a-2*b*b)*co*sn
    c0 = b*b*sn*sn+a*a*co*co
    d0 = (2*b*b-2*a*a)*d*co*sn-2*c*(b*b*co*co+a*a*sn*sn)
    e0 = (2*b*b-2*a*a)*c*co*sn-2*d*(a*a*co*co+b*b*sn*sn)
    f0 = (b*b*c*c+a*a*d*d)*co*co+(a*a*c*c+b*b*d*d) * \
        sn*sn+(2*a*a-2*b*b)*d*c*co*sn-a*a*b*b
    a = b0/a0
    b = c0/a0
    c = d0/a0
    d = e0/a0
    e = f0/a0
    return (a, b, c, d, e)


def get_arc_axis_and_angle_2D(arc: Arc, isRela=False) -> list:
    # transfer to XoY relative plane.
    if (not is_two_dimensional_matrix(arc.transformation)) and \
       (not is_shadow_matrix_on_xoy(arc.transformation)):
        raise TypeError('arc must locate on XoY!')
    forwM = get_orthogonal_matrix(arc.transformation)
    arcR = inverse_orth(forwM)*arc  # relative coordinate
    mat = arcR.transformation
    a11 = mat._mat[0][0]
    a12 = mat._mat[0][1]
    a21 = mat._mat[1][0]
    a22 = mat._mat[1][1]
    # g_axisO ellipse general formula: Ax^2+Bxy+Cy^2+Dx+Ey+1==0
    deno = (a12*a21-a11*a22)*(a12*a21-a11*a22)
    A = -(a21*a21+a22*a22)/deno
    B = 2*(a21*a11+a12*a22)/deno
    C = -(a12*a12+a11*a11)/deno
    # D=E=0, xc=yc=0
    a = sqrt(-2/(A+C+sqrt((A-C)*(A-C)+B*B)))
    b = sqrt(-2/(A+C-sqrt((A-C)*(A-C)+B*B)))
    theta = 1/2*atan2(B, (A-C))
    if not isRela:
        thetaS = get_angle_of_two_vectors(g_axisX, arcR.pointStart)
        theta = theta+thetaS
    return (a, b, theta)


# 从二维Arc提取旋转角(不支持镜像Arc)
def get_arc_rotate_angle_2D(arc: Arc, isHoriz=False) -> list:
    # rotz(thetaL)*scale(a,b)*rotz(thetaR)*Arc() = Tm
    # thetaL is whole arc rotate angle, thetaR is arc start angle.
    def _inverse_2x2(a, b, c, d):  # 2*2 matrix inverse
        if abs(a*d-b*c) < PL_A:  # |A|==0
            return [[0, 0], [0, 0]]
        det = 1/(a*d-b*c)
        inv = [[det*d, -det*b], [-det*c, det*a]]
        return inv
    if (not is_two_dimensional_matrix(arc.transformation)) and \
       (not is_shadow_matrix_on_xoy(arc.transformation)):
        raise TypeError('arc must locate on XoY!')
    m1 = arc.transformation._mat[0][0]
    m2 = arc.transformation._mat[0][1]
    m3 = arc.transformation._mat[1][0]
    m4 = arc.transformation._mat[1][1]
    if abs(m1-m4) < PL_A and abs(m3+m2) < PL_A:  # is circle
        thetaR = atan2(m3-m2, m1+m4)  # singular point
        thetaL = 0.0
        sx = sy = sqrt((m3-m2)*(m3-m2)+(m1+m4) * (m1+m4))/2
        return (sx, sy, thetaL, thetaR)
    D1 = atan2(m3-m2, m1+m4)  # thetaL+thetaR
    D0 = atan2(m2+m3, m1-m4)  # thetaL-thetaR
    thetaL = (D1+D0)/2  # left side
    thetaR = (D1-D0)/2  # right side
    if abs(thetaL+thetaR) < PL_A and abs(thetaL-thetaR) < PL_A:
        sx = m1
        sy = m4
    elif abs(thetaL+thetaR) < PL_A:
        inv = _inverse_2x2(1, 1, cos(thetaL)**2, sin(thetaR)**2)
        sx = inv[0][0]*(m1+m4)+inv[0][1]*m1
        sy = inv[1][0]*(m1+m4)+inv[1][1]*m1
    elif abs(thetaL-thetaR) < PL_A:
        inv = _inverse_2x2(1, -1, cos(thetaL)**2, -sin(thetaR)**2)
        sx = inv[0][0]*(m1-m4)+inv[0][1]*m1
        sy = inv[1][0]*(m1-m4)+inv[1][1]*m1
    else:
        sx = ((m3-m2)/sin(thetaL+thetaR)+(m2+m3)/sin(thetaL-thetaR))/2
        sy = ((m3-m2)/sin(thetaL+thetaR)-(m2+m3)/sin(thetaL-thetaR))/2
    if isHoriz and abs(abs(thetaL)-pi/2) < PL_A:
        t = sx  # if arc isnot horizontal, exchange sx and sy.
        sx = sy
        sy = t
        thetaL = 0
    return (abs(sx), abs(sy), thetaL, thetaR)


def get_three_points_from_arc(arc: Arc) -> list:  # 从arc中取3个点（起点-中点-终点）
    pointMiddle = arc.transformation * \
        GeVec3d(cos(arc.scope/2), sin(arc.scope/2), 0)
    return [arc.pointStart, pointMiddle, arc.pointEnd]
