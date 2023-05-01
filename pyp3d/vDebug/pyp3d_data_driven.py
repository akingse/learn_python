from .pyp3d_modeling import *

# import sympy
import re


# ------------------------------------------------------------------------------------------
# |                                    点线面几何约束                                        |
# |                         constraint of point-line-plane                                 |
# ------------------------------------------------------------------------------------------


# 点沿plane法线方向在plane上的投影
def get_shadow_point_along_normal_on_plane(point: GeVec3d, plane: GeTransform) -> GeVec3d:
    invM = inverse_std(get_orthogonal_matrix(plane))*trans(point)
    pointR = plane*to_vec2(get_matrixs_position(invM))
    return pointR


# 二维投影坐标系规则，是否允许用户自定义
# 二维平面将有默认的的坐标系，规则如下:
# 一般的，坐标系原点和坐标系x/y轴为世界坐标的投影，做叉乘处理；
# 当矢量投影为点或矢量共线时，将采用特殊处理;
def get_two_dimensional_reference_plane(anyPlane: GeTransform) -> GeTransform:
    pointO = get_shadow_point_along_normal_on_plane(g_axisO, anyPlane)
    pointX = get_shadow_point_along_normal_on_plane(g_axisX, anyPlane)
    pointY = get_shadow_point_along_normal_on_plane(g_axisY, anyPlane)
    if norm(pointX-pointO) < PL_A:  # pointX coincident, when YoZ plane
        return roty(-pi/2)
    if norm(pointY-pointO) < PL_A:  # pointX coincident, when XoZ plane
        return rotx(pi/2)
    if norm(cross(pointX, pointY)) < PL_A:  # plane through g_axisZ
        poseM = get_matrix_from_two_vectors(pointX-pointO, g_axisZ)
    else:  # general form
        poseM = get_matrix_from_two_vectors(pointX-pointO, pointY-pointO)
    return trans(pointO)*poseM


def constraint_point_on_line(point: GeVec3d, segm: Segment, d=0) -> GeTransform:
    # segm为约束直线（有起点，有方向）
    # point为被约束点
    # d为欠约束的距离变量
    return trans(segm.start-point)*trans(d*unitize(segm.vector))


# 使segmFree与约束直线segmFix重合
# d和theta为欠约束变量
def constraint_line_on_line(segmFree: Segment, segmFix: Segment, d=0, theta=0) -> GeTransform:
    transOri = constraint_point_on_line(segmFree.start, segmFix)
    angleIn = abs(get_angle_of_two_vectors(segmFree.vector, segmFix.vector))
    colliMat = rotate_arbitrary(segmFix.start, cross(
        segmFree.vector, segmFix.vector), angleIn)*transOri  # collinear matrix
    return rotate_arbitrary(segmFix.start, segmFix.vector, theta)*trans(d*unitize(segmFix.vector))*colliMat


# xy的值为二维坐标系的坐标值
def constraint_point_on_plane(point: GeVec3d, plane: GeTransform, x=0, y=0) -> GeTransform:
    plane2D = get_two_dimensional_reference_plane(plane)
    # show_coordinate_system(plane2D)
    pointSha = get_shadow_point_along_normal_on_plane(point, plane2D)
    return plane2D*trans(x, y)*inverse_std(plane2D)*trans(pointSha)


# thetaZ为二维平面z轴
def constraint_line_on_plane(segm: Segment, plane: GeTransform, x=0, y=0, thetaZ=0, thetaSelf=0) -> GeTransform:
    plane2D = get_two_dimensional_reference_plane(plane)
    pointShaStart = get_shadow_point_along_normal_on_plane(segm.start, plane2D)
    pointShaEnd = get_shadow_point_along_normal_on_plane(segm.end, plane2D)
    # show_coordinate_system(plane2D)
    if norm(pointShaStart-pointShaEnd) < PL_A:
        axisX = get_matrixs_axisx(plane2D)
        segmFix = Segment(pointShaStart, pointShaStart+axisX)
    else:
        segmFix = Segment(pointShaStart, pointShaEnd)
    colliMat = constraint_line_on_line(segm, segmFix, 0, thetaSelf)
    transR = plane2D*trans(x, y)*inverse_std(plane2D)
    rotAb = rotate_arbitrary(get_matrixs_position(plane2D),
                             get_matrixs_axisz(plane2D), thetaZ)
    return transR*rotAb*colliMat


# thetaZ为二维平面z轴
def constraint_plane_on_plane(planeFree: GeTransform, planeFix: GeTransform, x=0, y=0, thetaZ=0) -> GeTransform:
    plane2D = get_two_dimensional_reference_plane(planeFix)
    transR = plane2D*trans(x, y)*inverse_std(plane2D)
    rotAb = rotate_arbitrary(get_matrixs_position(plane2D),
                             get_matrixs_axisz(plane2D), thetaZ)
    return transR*rotAb*plane2D*planeFree


# ------------------------------------------------------------------------------------------
# |                            多表象几何算法 geometry multi_repre alg                       |
# ------------------------------------------------------------------------------------------


# 修改cube的长宽高
def setCubeLengthWidthHeight(cube, length=0, width=0, height=0) -> GeTransform:
    axisx = get_matrixs_axisx(cube.transformation)
    axisy = get_matrixs_axisy(cube.transformation)
    axisz = get_matrixs_axisz(cube.transformation)
    position = get_matrixs_position(cube.transformation)
    mat = set_matrix_by_column_vectors(
        length*axisx.unitize(), width*axisy.unitize(), height*axisz.unitize(), position)
    return mat


def getVertexByIndex(cube, indexes: list = []) -> list:
    mat = cube.transformation
    p0 = mat*GeVec3d(0, 0, 0)
    p1 = mat*GeVec3d(1, 0, 0)
    p2 = mat*GeVec3d(1, 1, 0)
    p3 = mat*GeVec3d(0, 1, 0)
    p4 = mat*GeVec3d(0, 0, 1)
    p5 = mat*GeVec3d(1, 0, 1)
    p6 = mat*GeVec3d(1, 1, 1)
    p7 = mat*GeVec3d(0, 1, 1)
    vertexList = [p0, p1, p2, p3, p4, p5, p6, p7]
    if len(indexes) == 0:
        return vertexList
    resList = []
    for iter in indexes:
        if iter >= 0 and iter < 8:  # else raise error
            resList.append(vertexList[iter])
    return resList


def setVertexByIndex(cube, index, vertex) -> GeTransform:
    # position = get_matrixs_position(mat)
    vertexList = getVertexByIndex(cube)
    # show_points_line(vertexList)
    vertexOri = vertexList[index]
    return trans(vertex-vertexOri)


def setVertexByIndexMulti(cube, vertexesList) -> GeTransform:
    mat = cube.transformation
    indexA = vertexesList[0][0]
    indexB = vertexesList[1][0]
    vertexA = getVertexByIndex(cube)[indexA]
    vertexB = getVertexByIndex(cube)[indexB]
    axisx = get_matrixs_axisx(mat).norm()
    axisy = get_matrixs_axisy(mat).norm()
    axisz = get_matrixs_axisz(mat).norm()
    lengthAB = norm(vertexA-vertexB)
    vertexANew = vertexesList[0][1]
    vertexBNew = vertexesList[1][1]
    normAB = norm(vertexBNew-vertexANew)
    k = normAB/lengthAB
    matStr = mat*scale(k)*inverse(mat)
    # create_geometry(matStr*cube)
    # new alg
    pose = inverse_std(get_orthogonal_matrix(mat))
    n = 3
    vertexAR = pose*vertexANew
    vertexBR = pose*vertexBNew
    # show_points_line([vertexA, vertexANew])
    # show_points_line([vertexB, vertexBNew])
    if n == 1:  # body dia
        matR = trans(vertexANew-vertexA)*get_orthogonal_matrix(mat) * \
            scale(vertexBR-vertexAR)
    elif n == 2:  # same segment # axis X p0 and p1 default
        matR = get_orthogonal_matrix(mat) * \
            scale(norm(vertexBR-vertexAR), axisy, axisz)
        matR = trans(vertexANew-vertexA)*matR
        matR = rotate_arbitrary(vertexANew, cross(
            vertexBNew-vertexANew, vertexB-vertexA), -abs(get_angle_of_two_vectors(vertexBNew-vertexANew, vertexB-vertexA)))*matR
    elif n == 3:  # vertex p0 and p2 default
        diag = vertexBR-vertexAR
        # the lean seciont, roty
        scX = sqrt(diag.x*diag.x+diag.z*diag.z)
        scY = abs(diag.y)
        leanS = scale(scX, scY, axisz)
        # the lean seciont, rotx
        # scX = abs(diag.x)
        # scY = sqrt(diag.y*diag.y+diag.z*diag.z)
        matR = get_orthogonal_matrix(mat) * rotz(atan(axisy/axisx))  # * leanS
        matR = trans(vertexANew-vertexA)*matR
        diagAB = vertexB-vertexA
        diagABNew = vertexBNew-vertexANew
        matR = rotate_arbitrary(vertexANew, cross(
            diagABNew, diagAB), -abs(get_angle_of_two_vectors(diagABNew, diagAB)))*matR
        matR = matR * rotz(-atan(scY/scX)) * leanS

    newVertex = getVertexByIndex(matR*Cube())
    # create_geometry(matR*Cube())
    # show_coordinate_system(get_orthogonal_matrix(matR))
    return


# ------------------------------------------------------------------------------------------
# |                               C++ call Python calculate                                |
# ------------------------------------------------------------------------------------------

# 计算表达式数值
def get_calculate_value(expre) -> float:
    try:
        return float(eval(expre))
    except:
        return float("nan")


# 计算矢量表达式数值
def get_calculate_vector(expre) -> GeVec3d:
    # format:split by english comma symbol: "20+10,0+1,3+4"
    g_axisNaN = GeVec3d(float("nan"), float("nan"), float("nan"))
    try:
        coord = expre.split(',')
        if len(coord) == 1:
            return GeVec3d(eval(coord[0]))
        if len(coord) == 2:
            return GeVec3d(eval(coord[0]), eval(coord[1]))
        if len(coord) == 3:
            return GeVec3d(eval(coord[0]), eval(coord[1]), eval(coord[2]))
        else:
            return g_axisNaN
    except:
        return g_axisNaN


# 计算表达式反函数
def get_inverse_function_value(expre) -> str:
    from sympy.abc import x, y
    try:  # double check, ensure itis correct expression
        res = eval("lambda {}:{}".format("x", expre))
        fy = sympy.solve(res(x)-y, x)
        fys = re.sub(r'\[|\]', '', str(fy))
        return fys
    except:
        return ""


# 计算矢量表达式反函数
def get_inverse_function_vector(expre) -> str:
    try:  # double check, ensure itis correct expression
        from sympy.abc import x, y
        glo = globals()  # loc = locals()
        vecMap = dict()
        expreCopy = expre  # copy expre, to record new expre
        iter = re.finditer("vec\(.+?\)", expre)
        n = 0
        for match in iter:
            finder = match.group()
            finderAdd = re.sub("\(", "\(", finder)
            finderAdd = re.sub("\)", "\)", finderAdd)
            key = "_c"+str(n)
            n += 1
            vecMap[key] = finder
            expreCopy = re.sub(finderAdd, key, expreCopy)
        # process smybol calcul
        symList = str()  # all symbols
        comd = str()  # command to executed
        for i in range(n):
            # symList += "_c"+str(i)+","
            if i != n-1:
                symList += "_c"+str(i)+","
            else:
                symList += "_c"+str(i)
        comd = symList+"= sympy.abc.symbols('"+symList+"')"
        if n != 0:
            exec(comd, globals())
        fx = eval("lambda {}:{}".format("x,"+symList, expreCopy))
        comd = "fy = sympy.solve(fx(x,"+symList+")-y, x)"
        exec(comd, locals(), globals())
        fys = glo["fy"]
        fysExp = re.sub(r'\[|\]', '', str(fys))
        # sub original vectors
        iter = re.finditer("_c\d", fysExp)
        for match in iter:
            finder = match.group()
            fysExp = re.sub(finder, vecMap[finder], fysExp)
        return fysExp
    except:
        return ""
