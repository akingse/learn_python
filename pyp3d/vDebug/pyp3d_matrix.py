# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 矩阵操作函数方法
# Author: YouQi, akingse
# Date: 2021/08/07
from .pyp3d_vector import *

# ------------------------------------------------------------------------------------------
# |                                         BASIS                                          |
# ------------------------------------------------------------------------------------------


def scale(*args) -> GeTransform:  # 缩放矩阵
    '''
    Genetate a scale zoom transform matrix
    '''
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    else:
        args = list(args)
    if len(args) == 0:
        return g_matrixE  # g_matrixO
    elif len(args) == 1:
        if isinstance(args[0], (int, float)):
            return GeTransform([[args[0], 0, 0, 0], [0, args[0], 0, 0], [0, 0, args[0], 0]])
        elif isinstance(args[0], GeVec2d):
            return GeTransform([[args[0].x, 0, 0, 0], [0, args[0].y, 0, 0], [0, 0, 1, 0]])
        elif isinstance(args[0], GeVec3d):
            return GeTransform([[args[0].x, 0, 0, 0], [0, args[0].y, 0, 0], [0, 0, args[0].z, 0]])
        else:
            raise ValueError('improper parameter!')
    elif len(args) == 2:
        return GeTransform([[args[0], 0, 0, 0], [0, args[1], 0, 0], [0, 0, 1, 0]])
    elif len(args) == 3:
        return GeTransform([[args[0], 0, 0, 0], [0, args[1], 0, 0], [0, 0, args[2], 0]])
    else:
        raise ValueError('improper parameter!')


def scalex(x: float = 1) -> GeTransform:  # 沿x方向缩放
    return GeTransform([[x, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])


def scaley(y: float = 1) -> GeTransform:  # 沿y方向缩放
    return GeTransform([[1, 0, 0, 0], [0, y, 0, 0], [0, 0, 1, 0]])


def scalez(z: float = 1) -> GeTransform:  # 沿z方向缩放
    return GeTransform([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, z, 0]])


def scale_xoy(s: float = 1) -> GeTransform:  # 沿xy方向缩放
    return GeTransform([[s, 0, 0, 0], [0, s, 0, 0], [0, 0, 1, 0]])


def scale_point(point: GeVec3d = g_axisO, x: float = 1, y: float = 1, z: float = 1) -> GeTransform:  # 以点为中心进行缩放
    return trans(point)*scale(x, y, z)*trans(-point)


def trans(*args) -> GeTransform:  # 平移矩阵
    '''
    Genetate a translation transform matrix
    '''
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = list(args[0])
    else:
        args = list(args)
    if len(args) == 0:
        return g_matrixE
    elif len(args) == 1:
        if isinstance(args[0], (int, float)):
            return GeTransform([[1, 0, 0, args[0]], [0, 1, 0, 0], [0, 0, 1, 0]])
        elif isinstance(args[0], GeVec3d):
            return GeTransform([[1, 0, 0, args[0].x], [0, 1, 0, args[0].y], [0, 0, 1, args[0].z]])
        elif isinstance(args[0], GeVec2d):
            return GeTransform([[1, 0, 0, args[0].x], [0, 1, 0, args[0].y], [0, 0, 1, 0]])
        else:
            raise ValueError('improper parameter!')
    elif len(args) == 2:
        return GeTransform([[1, 0, 0, args[0]], [0, 1, 0, args[1]], [0, 0, 1, 0]])
    elif len(args) == 3:
        return GeTransform([[1, 0, 0, args[0]], [0, 1, 0, args[1]], [0, 0, 1, args[2]]])
    else:
        raise ValueError('improper parameter!')


def transx(x: float = 0) -> GeTransform:  # 沿x方向平移
    return GeTransform([[1, 0, 0, x], [0, 1, 0, 0], [0, 0, 1, 0]])


def transy(y: float = 0) -> GeTransform:  # 沿y方向平移
    return GeTransform([[1, 0, 0, 0], [0, 1, 0, y], [0, 0, 1, 0]])


def transz(z: float = 0) -> GeTransform:  # 沿z方向平移
    return GeTransform([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z]])


def rotate(*args) -> GeTransform:  # 轴角表示法的旋转矩阵
    '''
    Generate a rotation transform matrix, using axis-angle method (radian)
    '''
    if len(args) == 0:
        return GeTransform()
    elif len(args) == 1 and isinstance(args[0], (GeVec2d, GeVec3d)):
        return GeTransform()
    elif len(args) == 1 and isinstance(args[0], (int, float)):
        nv, angle = g_axisZ, float(args[0])
    elif len(args) == 2:
        if isinstance(args[0], GeVec3d) and isinstance(args[1], (int, float)):
            nv, angle = unitize(args[0]), float(args[1])
        elif isinstance(args[1], GeVec3d) and isinstance(args[0], (int, float)):
            nv, angle = unitize(args[1]), float(args[0])
        else:
            raise TypeError('improper parameter!')
    else:
        raise ValueError('improper parameter!')
    # Rodrigues' rotation formula
    c, s = 1-cos(angle), sin(angle)
    T = GeTransform([[0.0, -nv.z*c, nv.y*c, 0.0], [nv.z*c, 0.0, -nv.x*c, 0.0], [-nv.y*c, nv.x*c, 0.0, 0.0]]) * \
        GeTransform([[0.0, -nv.z, nv.y, 0.0],
                    [nv.z, 0.0, -nv.x, 0.0], [-nv.y, nv.x, 0.0, 0.0]])
    return GeTransform([[T._mat[0][0]+1.0, T._mat[0][1]-nv.z*s, T._mat[0][2]+nv.y*s, 0.0],
                        [T._mat[1][0]+nv.z*s, T._mat[1][1] +
                            1.0, T._mat[1][2]-nv.x*s, 0.0],
                        [T._mat[2][0]-nv.y*s, T._mat[2][1]+nv.x*s, T._mat[2][2]+1.0, 0.0]])


# 绕过point点的vector矢量,旋转theta弧度
def rotate_arbitrary(point: GeVec3d = g_axisO, vector: GeVec3d = g_axisZ, theta: float = 0) -> GeTransform:
    '''
    appoint arbitrary point and arbitrary vector to rotate
    '''
    f = unitize(vector)
    c, s = cos(theta), sin(theta)
    T = GeTransform([[f.x*f.x*(1-c)+c, f.x*f.y*(1-c)-f.z*s, f.x*f.z*(1-c)+f.y*s, 0],
                    [f.x*f.y*(1-c)+f.z*s, f.y*f.y*(1-c) +
                     c, f.y*f.z*(1-c)-f.x*s, 0],
                    [f.x*f.z*(1-c)-f.y*s, f.y*f.z*(1-c)+f.x*s, f.z*f.z*(1-c)+c, 0]])
    return trans(point)*T*trans((-1.0)*point)
    # return trans(point)*rotate(vector,theta)*trans(-point)


# 基本旋转矩阵
def rotx(theta=0) -> GeTransform:  # 仅绕世界坐标系X轴的旋转
    return GeTransform([[1, 0, 0, 0], [0, cos(theta), -sin(theta), 0], [0, sin(theta), cos(theta), 0]])


def roty(theta=0) -> GeTransform:  # 仅绕世界坐标系Y轴的旋转
    return GeTransform([[cos(theta), 0, sin(theta), 0], [0, 1, 0, 0], [-sin(theta), 0, cos(theta), 0]])


def rotz(theta=0) -> GeTransform:  # 仅绕世界坐标系Z轴的旋转
    return GeTransform([[cos(theta), -sin(theta), 0, 0], [sin(theta), cos(theta), 0, 0], [0, 0, 1, 0]])


def mirror(mat: GeTransform = g_matrixE, plane="YoZ") -> GeTransform:  # 关于平面的镜像矩阵
    mirXOY = GeTransform([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0]])
    mirXOZ = GeTransform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0]])
    mirYOZ = GeTransform([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
    if plane == "xy" or plane == "xoy" or plane == "XY" or plane == "XoY" or plane == "XOY":
        return mat*mirXOY*inverse(mat)
    elif plane == "xz" or plane == "xoz" or plane == "XZ" or plane == "XoZ" or plane == "XOZ":
        return mat*mirXOZ*inverse(mat)
    elif plane == "yz" or plane == "yoz" or plane == "YZ" or plane == "YoZ" or plane == "YOZ":
        return mat*mirYOZ*inverse(mat)
    else:
        raise TypeError('mirror_plane string param error!')


def mirror_xoy(mat: GeTransform = g_matrixE) -> GeTransform:  # 关于坐标系XOY平面镜像
    return mirror(mat, "XOY")


def mirror_xoz(mat: GeTransform = g_matrixE) -> GeTransform:  # 关于坐标系XOZ平面镜像
    return mirror(mat, "XOZ")


def mirror_yoz(mat: GeTransform = g_matrixE) -> GeTransform:  # 关于坐标系YOZ平面镜像
    return mirror(mat, "YOZ")


def mirror_axis(axis: GeVec3d) -> GeTransform:  # 关于轴镜像
    if not isinstance(axis, GeVec3d):
        raise TypeError('mirror unsupported!')
    if is_two_vectors_same_direction(g_axisX, axis) == "DIRECTION_SAME":
        return GeTransform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0]])
    elif is_two_vectors_same_direction(g_axisY, axis) == "DIRECTION_SAME":
        return GeTransform([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0]])
    elif is_two_vectors_same_direction(g_axisZ, axis) == "DIRECTION_SAME":
        return GeTransform([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0]])
    elif norm(axis) < PL_A:  # mirror about origin point
        return GeTransform([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0]])
    else:
        raise TypeError('Must assign proper axis!')


def shear(axis, *, x=0, y=0, z=0) -> GeTransform:  # 三维错切矩阵
    # * enforce using keyword to pass args
    # return GeTransform([[1,b,c,0],[d,1,f,0],[g,h,1,0]])
    if isinstance(axis, GeVec3d):  # assign axis
        if is_two_vectors_same_direction(g_axisX, axis) == "DIRECTION_SAME":
            return GeTransform([[1, 0, 0, 0], [y, 1, 0, 0], [z, 0, 1, 0]])
        elif is_two_vectors_same_direction(g_axisY, axis) == "DIRECTION_SAME":
            return GeTransform([[1, x, 0, 0], [0, 1, 0, 0], [0, z, 1, 0]])
        elif is_two_vectors_same_direction(g_axisZ, axis) == "DIRECTION_SAME":
            return GeTransform([[1, 0, x, 0], [0, 1, y, 0], [0, 0, 1, 0]])
        else:
            raise TypeError('please input proper argument!')
    else:
        raise TypeError('please input proper argument!')


def shearx(y: float = 0, z: float = 0) -> GeTransform:  # 拉伸x轴
    return GeTransform([[1, y, z, 0], [0, 1, 0, 0], [0, 0, 1, 0]])


def sheary(x: float = 0, z: float = 0) -> GeTransform:  # 拉伸y轴
    return GeTransform([[1, 0, 0, 0], [x, 1, z, 0], [0, 0, 1, 0]])


def shearz(x: float = 0, y: float = 0) -> GeTransform:  # 拉伸z轴
    return GeTransform([[1, 0, 0, 0], [0, 1, 0, 0], [x, y, 1, 0]])

# ------------------------------------------------------------------------------------------
# |                                        PROPERTY                                        |
# ------------------------------------------------------------------------------------------


def transpose(M: GeTransform, onlyRot=True) -> GeTransform:  # 获取矩阵的转置（姿态矩阵专用）
    # if not is_attitude_matrix(M):
    #     raise TypeError('must be unit attitude matrix!')
    matrix = GeTransform([[M._mat[0][0], M._mat[1][0], M._mat[2][0], 0*M._mat[0][3]],
                          [M._mat[0][1], M._mat[1][1], M._mat[2][1], 0*M._mat[1][3]],
                          [M._mat[0][2], M._mat[1][2], M._mat[2][2], 0*M._mat[2][3]]])
    return matrix


def inverse_orth(M: GeTransform) -> GeTransform:  # 正交变换矩阵的逆矩阵
    # if not is_orthogonal_matrix(M):
    #     return inverse(M)
    rotM = get_matrixs_rotation(M)
    posM = get_matrixs_position(M)
    return transpose(rotM)*trans((-1.0)*posM)


def inverse(M: GeTransform) -> GeTransform:  # 计算矩阵的逆矩阵
    '''
    generate a inverse matrix of the input GeTransform matrix
    '''
    if is_orthogonal_matrix(M):
        return inverse_orth(M)
    # if not isinstance(M,GeTransform):
    #     raise TypeError('parameter must be matrix!')
    T_inv = GeTransform(
        [[1, 0, 0, -M._mat[0][3]], [0, 1, 0, -M._mat[1][3]], [0, 0, 1, -M._mat[2][3]]])
    a11 = M._mat[0][0]
    a12 = M._mat[0][1]
    a13 = M._mat[0][2]
    a21 = M._mat[1][0]
    a22 = M._mat[1][1]
    a23 = M._mat[1][2]
    a31 = M._mat[2][0]
    a32 = M._mat[2][1]
    a33 = M._mat[2][2]
    M_det = a11*a22*a33 + a12*a23*a31 + a13*a32 * \
        a21 - a13*a22*a31 - a12*a21*a33 - a11*a32*a23
    if abs(M_det) < PL_A:
        print("ValueError: matrix determinant value is zero!")
        # raise ValueError('matrix determinant value is zero!')
        return g_matrixO
    b11 = a22*a33-a23*a32
    b12 = a21*a33-a23*a31
    b13 = a21*a32-a22*a31
    b21 = a12*a33-a13*a32
    b22 = a11*a33-a13*a31
    b23 = a11*a32-a12*a31
    b31 = a12*a23-a13*a22
    b32 = a11*a23-a13*a21
    b33 = a11*a22-a12*a21
    M_adj = GeTransform([[b11, -b21, b31, 0],  # been transposed matrix
                         [-b12, b22, -b32, 0],
                         [b13, -b23, b33, 0]])
    return (1/M_det)*M_adj*T_inv

# ------------------------------------------------------------------------------------------
# |                                        SET&GET                                         |
# ------------------------------------------------------------------------------------------


def set_matrix_by_column_vectors(vecX:GeVec3d, vecY:GeVec3d, vecZ:GeVec3d, p=GeVec3d(0, 0, 0)) -> GeTransform:  # 通过列矢量创建矩阵
    matrix = GeTransform([[vecX.x, vecY.x, vecZ.x, p.x],
                          [vecX.y, vecY.y, vecZ.y, p.y],
                          [vecX.z, vecY.z, vecZ.z, p.z]])
    return matrix


def set_matrix_by_row_vectors(vecA:GeVec3d, vecB:GeVec3d, vecC:GeVec3d, p=GeVec3d(0, 0, 0)) -> GeTransform:  # 通过行矢量创建矩阵
    matrix = GeTransform([[vecA.x, vecA.y, vecA.z, p.x],
                          [vecB.x, vecB.y, vecB.z, p.y],
                          [vecC.x, vecC.y, vecC.z, p.z]])
    return matrix


# 获取矩阵元素，返回1*12列表
def get_list_from_matrix(mat: GeTransform, isRow=True) -> list:
    alist = []
    if isRow:
        for i in range(3):
            for j in range(4):
                alist.append(mat._mat[i][j])
    else:
        for i in range(4):
            for j in range(3):
                alist.append(mat._mat[j][i])
    return alist


def get_matrixs_pose_row_vectors(M: GeTransform) -> list:  # 获取矩阵姿态行向量
    a = GeVec3d(M._mat[0][0], M._mat[0][1], M._mat[0][2])
    b = GeVec3d(M._mat[1][0], M._mat[1][1], M._mat[2][2])
    c = GeVec3d(M._mat[2][0], M._mat[2][1], M._mat[2][2])
    return (a, b, c)


def set_matrix_by_rot_trans(rot: GeTransform, position: GeVec3d) -> GeTransform:  # 通过旋转和平移创建矩阵
    # compat point and matrix, prefer point.
    if isinstance(position, (GeVec2d, GeVec3d)):
        return trans(position)*rot
    elif isinstance(position, GeTransform):
        return position*rot
    else:
        raise TypeError('function parameter type error!')


def get_matrixs_rotation(M: GeTransform) -> GeTransform:  # 获取矩阵的旋转部分，平移参数置零
    matrix = GeTransform([[M._mat[0][0], M._mat[0][1], M._mat[0][2], 0],
                          [M._mat[1][0], M._mat[1][1], M._mat[1][2], 0],
                          [M._mat[2][0], M._mat[2][1], M._mat[2][2], 0]])
    return matrix


# xyz欧拉角求逆解，mat=rotx(t1)*roty(t2)*rotz(t3)
def get_rot_matrix_angle_euler(M: GeTransform)->tuple:
    nx = M._mat[0][0]
    ny = M._mat[1][0]
    ox = M._mat[0][1]
    oy = M._mat[1][1]    
    ax = M._mat[0][2]
    ay = M._mat[1][2]
    az = M._mat[2][2]
    if (not is_float_zero(ax)):
        theta2=atan2(ax, sqrt(nx*nx+ox*ox)) # two solutions
        if (not is_float_zero(cos(theta2))):
            theta3=atan2(-ox/cos(theta2),nx/cos(theta2))
            theta1=atan2(-ay/cos(theta2),az/cos(theta2))
        else:
            theta13=atan2(ny,oy)
            theta1=theta13
            theta3=0.0
    else:
        theta2=0.0
        theta1=atan2(-ay,az)
        theta3=atan2(-ox,nx)
    return (theta1,theta2,theta3)

def get_rot_matrix_angle(M: GeTransform) -> tuple:  # 获取(单位)旋转矩阵的逆变换(ZYZ欧拉角)
    nx = M._mat[0][0]
    ny = M._mat[1][0]
    nz = M._mat[2][0]
    # ox=m._mat[0][1]
    # oy=m._mat[1][1]
    oz = M._mat[2][1]
    ax = M._mat[0][2]
    ay = M._mat[1][2]
    az = M._mat[2][2]
    # theta2=atan2(-sqrt(nz**2+oz**2),az) # one root of two groups.
    theta2 = atan2(sqrt(nz**2+oz**2), az)
    if abs(theta2) < PL_A:
        theta1 = atan2(ny, nx)
        theta3 = 0
    else:
        s5 = sin(theta2)
        theta3 = atan2(oz/s5, -nz/s5)
        theta1 = atan2(ay/s5, ax/s5)
    return (theta1, theta2, theta3)


def get_matrixs_position(M: GeTransform) -> GeVec3d:  # 获取矩阵的平移参数
    return GeVec3d(M._mat[0][3], M._mat[1][3], M._mat[2][3])


def get_translate_matrix(M: GeTransform) -> GeTransform:  # 获取矩阵的平移矩阵
    return trans(get_matrixs_position(M))


def get_scale_param(M: GeTransform, isLeft=True) -> GeVec3d:  # 获取矩阵的缩放参数
    # left means the other transform matrix left multiply.
    if isLeft:
        a = sqrt(M._mat[0][0]**2+M._mat[1][0]**2+M._mat[2][0]**2)
        b = sqrt(M._mat[0][1]**2+M._mat[1][1]**2+M._mat[2][1]**2)
        c = sqrt(M._mat[0][2]**2+M._mat[1][2]**2+M._mat[2][2]**2)
    else:
        a = sqrt(M._mat[0][0]**2+M._mat[0][1]**2+M._mat[0][2]**2)
        b = sqrt(M._mat[1][0]**2+M._mat[1][1]**2+M._mat[1][2]**2)
        c = sqrt(M._mat[2][0]**2+M._mat[2][1]**2+M._mat[2][2]**2)
    return GeVec3d(a, b, c)


def get_scale_matrix(M: GeTransform, isLeft=True) -> GeTransform:  # 获取矩阵的缩放矩阵
    return scale(get_scale_param(M, isLeft))


def get_matrixs_axisx(M: GeTransform) -> GeVec3d:  # 获取矩阵的X轴分量（矢量原始值）
    return GeVec3d(M._mat[0][0], M._mat[1][0], M._mat[2][0])


def get_matrixs_axisy(M: GeTransform) -> GeVec3d:  # 获取矩阵的Y轴分量（矢量原始值）
    return GeVec3d(M._mat[0][1], M._mat[1][1], M._mat[2][1])


def get_matrixs_axisz(M: GeTransform) -> GeVec3d:  # 获取矩阵的Z轴分量（矢量原始值）
    return GeVec3d(M._mat[0][2], M._mat[1][2], M._mat[2][2])

# ------------------------------------------------------------------------------------------
# |                                         JUDGE                                          |
# ------------------------------------------------------------------------------------------


def is_identify_matrix(M: GeTransform) -> bool:  # 是否为单位矩阵
    pos = get_matrixs_position(M)
    if (norm(pos) > PL_A):
        return False
    for i in range(3):
        for j in range(3):
            if i == j and abs(M._mat[i][j]-1) > PL_A:
                return False
            elif i != j and abs(M._mat[i][j]) > PL_A:
                return False
    return True


def is_zero_matrix(M: GeTransform) -> bool:  # 是否为全零矩阵
    axisx = get_matrixs_axisx(M)
    axisy = get_matrixs_axisy(M)
    axisz = get_matrixs_axisz(M)
    axisp = get_matrixs_position(M)
    return norm(axisx)+norm(axisy)+norm(axisz)+norm(axisp) < PL_A


def is_orthogonal_matrix(M: GeTransform, onlyRot=True) -> bool:  # 判断一个矩阵是否为单位正交矩阵
    # onlyRot=True, only judge rotate part
    if onlyRot == False:  # there is no position param
        pos = get_matrixs_position(M)
        if (norm(pos) > PL_A):
            return False
    mat = get_matrixs_rotation(M)
    return is_identify_matrix(mat*transpose(mat))


def get_orthogonal_matrix(M: GeTransform, withTrans=True, is2D=False) -> GeTransform:  # 获取单位正交矩阵
    # is2D to control unit matrix while locate on XoY
    if is_orthogonal_matrix(M, withTrans):
        return M
    vec1 = get_matrixs_axisx(M)
    vec2 = get_matrixs_axisy(M)
    vectorX = unitize(vec1)
    vectorZ = unitize(cross(vec1, vec2))
    vectorY = unitize(cross(vectorZ, vectorX))
    mat = set_matrix_by_column_vectors(vectorX, vectorY, vectorZ)
    orth = get_translate_matrix(M)*mat if withTrans else mat
    return g_matrixE if (is2D and is_two_dimensional_matrix(mat)) else orth


def is_attitude_matrix(M: GeTransform) -> bool:  # 判断一个矩阵是否为单位姿态矩阵（仅旋转变换）
    # judeg whether position is zero.
    if abs(M._mat[0][3])+abs(M._mat[1][3])+abs(M._mat[2][3]) > PL_A:
        return False
    vec = get_scale_param(M)
    if abs(vec.x-1)+abs(vec.y-1)+abs(vec.z-1) > PL_A:
        return False
    axisx = get_matrixs_axisx(M)
    axisy = get_matrixs_axisy(M)
    axisz = get_matrixs_axisz(M)
    if is_two_vectors_same_direction(axisz, cross(axisx, axisy)) != "DIRECTION_SAME" or \
            is_two_vectors_same_direction(axisx, cross(axisy, axisz)) != "DIRECTION_SAME" or \
            is_two_vectors_same_direction(axisy, cross(axisz, axisx)) != "DIRECTION_SAME":  # three axes orthogonal judge.
        return False
    return True


# 是否为二维矩阵（仅rotz&trans(x,y)）
def is_two_dimensional_matrix(M: GeTransform) -> bool:
    vecx = get_matrixs_axisx(M)
    vecy = get_matrixs_axisy(M)
    pos = get_matrixs_position(M)
    if abs(pos.z) > PL_A:
        return False
    if abs(dot(vecx, g_axisZ)) > PL_A or abs(dot(vecy, g_axisZ)) > PL_A:
        return False
    return True


def is_shadow_matrix_on_xoy(M: GeTransform, withTrans=False) -> bool:
    pos = get_matrixs_position(M)
    if withTrans and norm(pos) > PL_A:
        return False
    a, b, c = M._mat[2][0], M._mat[2][1], M._mat[2][2]
    return abs(a)+abs(b)+abs(c) < PL_A


def is_rigid_matrix(M: GeTransform) -> bool:  # 判断一个矩阵是否为刚性位姿矩阵（仅平移旋转变换）
    rotPart = get_matrixs_rotation(M)
    if not is_attitude_matrix(rotPart):
        return False
    return True

# ------------------------------------------------------------------------------------------
# |                                        SHADOW                                          |
# ------------------------------------------------------------------------------------------


def shadow_parallel(pointQ=GeVec3d(0, 0, 0), vectorN=GeVec3d(0, 0, 1), uLight=GeVec3d(0, 0, 1)) -> GeTransform:  # 平行投影矩阵
    N = unitize(vectorN)
    u = unitize(uLight)
    k = 1/dot(u, N)
    M = GeTransform([[N.x*u.x, N.x*u.y, N.x*u.z, 0],
                     [N.y*u.x, N.y*u.y, N.y*u.z, 0],
                     [N.z*u.x, N.z*u.y, N.z*u.z, 0]])
    I_M = GeTransform()-k*M
    kq = dot(pointQ, vectorN)/dot(uLight, vectorN)
    return trans(kq*uLight)*I_M


def shadow_vector_matrix_2D(n: GeVec3d) -> GeTransform:  # arbitrary_shadow 矢量正投影
    matrix = GeTransform([[1-n.x**2, -n.x*n.y, -n.x*n.z, 0],
                          [-n.x*n.y, 1-n.y**2, -n.y*n.z, 0],
                          [-n.x*n.z, -n.y*n.z, 1-n.z**2, 0]])
    return matrix


def shadow_scale_matrix(intAngle=0) -> GeTransform:  # 绕Z轴放大投影矩阵
    return scale(1/cos(intAngle), 1/cos(intAngle), 1)*rotz(intAngle)


def is_shadow_matrix_on_xoy(M: GeTransform) -> bool:  # 是否为xoy平面的投影矩阵
    c = get_matrixs_pose_row_vectors(M)[2]
    return norm(c) < PL_A


def get_full_rank_matrix_from_shadow(M: GeTransform, withTrans=True) -> GeTransform:
    n = get_matrixs_axisx(M)
    o = get_matrixs_axisy(M)
    p = get_matrixs_position(M) if withTrans else g_axisO
    mat = set_matrix_by_column_vectors(n, o, g_axisZ, p)
    return mat


# 对于3-D空间的某平面做镜像,平面法向量u(x,y,z)
def get_mirror_matrix_by_planes_normal(u=GeVec3d(0, 0, 1)) -> GeTransform:
    x, y, z = u.x, u.y, u.z
    return GeTransform(
        [[1-2*x*x, -2*x*y, -2*x*z, 0],
         [-2*x*y, 1-2*x*x, -2*y*z, 0],
         [-2*x*z, -2*y*z, 1-2*x*x, 0]])
# 两点布置旋转矩阵


def get_trans_from_two_points(point1: GeVec3d, point2: GeVec3d) -> GeTransform:
    v12 = point1-point2
    v12_norm = norm(v12)
    if v12_norm != 0.0:
        angle_z = acos(v12.z/v12_norm)
        # if angle_z == 0.0:
        if abs(angle_z) < PL_A:
            transformation = rotate(GeVec3d(0, 1, 0),  -pi/2)
            return transformation
        # elif angle_z == pi:
        elif abs(abs(angle_z)-pi) < PL_A:
            transformation = rotate(GeVec3d(0, 1, 0),  pi/2)
            return transformation
        else:
            r_xy = sqrt(v12.x**2 + v12.y**2)
            angle_xy = acos(v12.x/r_xy)
            if v12.y < 0.0:
                angle_xy = -angle_xy
            transformation = rotate(GeVec3d(0, 0, 1),  angle_xy) * rotate(
                GeVec3d(0, 1, 0),  angle_z-pi/2)
            return transformation

def isAcuteAngle(vecA: GeVec3d, vecB: GeVec3d)->bool:
    return  vecA * vecB > 0

def hasMatrixMirror( M:GeTransform)->bool:
	axisx = get_matrixs_axisx(M)
	axisy = get_matrixs_axisy(M)
	axisz = get_matrixs_axisz(M)
	# support shear, on the basis of the dierction range of coord-axis
	return not (isAcuteAngle(axisx,axisy ^ axisz) and isAcuteAngle(axisy,axisz ^ axisx) and isAcuteAngle(axisz,axisx ^ axisy))
