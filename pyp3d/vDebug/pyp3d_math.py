# Copyright (C), 2019-2028, Beijing GLory PKPM Tech. Co., Ltd.
# Brief: PKPM-BIMBase Python二次开发SDK与参数化组件功能。
# 基本数学函数
# Author: akingse
# Date: 2021/02
from .pyp3d_data import *
from random import *

# ------------------------------------------------------------------------------------------
# |                                         MATH                                           |
# ------------------------------------------------------------------------------------------


def atan_posi(y, x) -> float:
    return atan2(y, x) if atan2(y, x) >= 0 else atan2(y, x)+2*pi


def appro_angle(x) -> float:
    return 0 if abs(x) < PL_A or abs(abs(x)-2*pi) < PL_A else x


# 浮点数取整
def appro_zero(num) -> float:
    return round(num/PL_E6)*PL_E6 if abs(abs(num /
                                             PL_E6)-round(abs(num/PL_E6))) <= PL_A/PL_E6 else num


def appro_num(num) -> float:
    numA = abs(round(num)-num)
    return round(num) if (numA) < PL_E6 else num


def appro_vector(vector):
    return GeVec3d(appro_num(vector.x), appro_num(vector.y), appro_num(
        vector.z)) if isinstance(vector, GeVec3d) else GeVec3d(appro_num(vector.x), appro_num(vector.y))


def appro_matrix(m: GeTransform) -> GeTransform:
    mat = GeTransform([[appro_num(m._mat[0][0]), appro_num(m._mat[0][1]), appro_num(m._mat[0][2]), appro_num(m._mat[0][3])],
                      [appro_num(m._mat[1][0]), appro_num(m._mat[1][1]), appro_num(
                          m._mat[1][2]), appro_num(m._mat[1][3])],
                       [appro_num(m._mat[2][0]), appro_num(m._mat[2][1]), appro_num(m._mat[2][2]), appro_num(m._mat[2][3])]])
    return mat


# auto float precision
def is_float_zero(num: float, eps=PL_A) -> bool:
    if not bool(eps):
        return not bool(num)  # manual set math 0
    return abs(num) < eps  # default


def is_float_equal(numA: float, numB: float, eps=0.0) -> bool:
    if not bool(eps):
        # default
        maxl = abs(numA) if abs(numA) > abs(numB) else abs(numB)
        return abs(numA - numB) < (maxl+1) * PL_A
    return abs(numA - numB) <= eps


def math_sign(x) -> float:  # sign符号函数
    if abs(x) < PL_A:
        return 0.0
    return float(1.0) if (x.real > 0) else float(-1.0)


# override base math funciton, to avoid floating devition.
def math_sqrt(x) -> float:
    return float(0.0) if (abs(x) < PL_A) else sqrt(x)


# pythagoras theorem
def math_pytha(a, b) -> float:
    return sqrt(a*a+b*b)

# ------------------------------------------------------------------------------------------
# |                                         TRIGON                                         |
# ------------------------------------------------------------------------------------------


def angle_posi(theta) -> float:
    return theta+2 * pi if theta < 0 else theta  # 弧度强转 0->2*pi


def angle_nega(theta) -> float:
    return theta-2 * pi if theta > 0 else theta  # 弧度强转 -2*pi->0


def math_acos(x) -> float:
    if abs(x-1.0) < PL_A:
        return 0.0
    elif abs(x+1.0) < PL_A:
        return pi
    else:
        return acos(x)


def arc_theta2alpha(theta, a, b) -> float:  # 圆心角转扫掠角
    # alpha means oval point angle
    return atan2(b*sin(theta), a*cos(theta))  # alpha


def arc_alpha2theta(alpha, a, b) -> float:  # 扫掠角转圆心角
    # theta means circle central angle
    return atan2(a*sin(alpha), b*cos(alpha))  # theta


# ------------------------------------------------------------------------------------------
# |                                        COMPLEX                                         |
# ------------------------------------------------------------------------------------------


def math_complex_power(x, a) -> complex:  # 复数指数运算
    if not isinstance(x, complex):
        return x**a
    r = abs(x)
    theta = atan2(x.imag, x.real)
    r = r**a
    theta = theta*a
    return r*complex(cos(theta), sin(theta))


def math_cublic_real_root(n) -> float:  # 开三次根号-实数根
    return n**(1/3) if (n >= 0) else -(-n)**(1/3)


def math_imag_sqrt(n) -> complex:  # 负数开平方-复数根
    if isinstance(n, complex):
        return math_complex_power(n, 1/2)
    else:
        return (sqrt(n)) if (n >= 0) else complex(0, sqrt(-n))


# ------------------------------------------------------------------------------------------
# |                                        EQUATION                                        |
# ------------------------------------------------------------------------------------------


# 解一元二次方程
def math_quadratic_equation(a, b, c, realRoot=True) -> list:
    # general formula: ax**2+bx+c=0
    if abs(a) < PL_A:
        return [] if(abs(b) < PL_A) else [-c/b]  # one unknown linear
        # raise ValueError('the denominator isnot zero!')
    delta = b*b-4*a*c
    if abs(delta) < PL_A:
        return [-b/(2*a)]
    elif delta < 0:
        d = complex(0, sqrt(-delta))  # only real root
        return [] if realRoot else [(-b+d)/(2*a), (-b-d)/(2*a)]
    else:
        d = sqrt(delta)
        return [(-b+d)/(2*a), (-b-d)/(2*a)]


# 解一元三次方程
def math_cardano_formula(a, b, c, d, realRoot=True) -> list:  # 卡尔丹公式，实根解
    # general formula:  ax**3+bx**2+cx+d=0 # realRoot
    if abs(a) < PL_A:  # compat quadratic_equation
        return math_quadratic_equation(b, c, d, realRoot)
    b = b/a
    c = c/a
    d = d/a  # a=1;
    p = -b**2/3+c
    q = (2*b**3)/27-(c*b)/3+d
    delta = (q/2)**2+(p/3)**3  # delta judge
    if delta >= 0:
        u = math_cublic_real_root(-q/2+math_imag_sqrt(delta))
        v = math_cublic_real_root(-q/2-math_imag_sqrt(delta))
    else:
        u = (-q/2+math_imag_sqrt(delta))**(1/3)
        v = (-q/2-math_imag_sqrt(delta))**(1/3)
    omega = complex(-1.0, sqrt(3))/2
    omega2 = complex(-1.0, -sqrt(3))/2
    x1 = u+v-b/3
    x2 = omega*u+omega2*v-b/3
    x3 = omega2*u+omega*v-b/3
    # cubic equation has one real root at least, itis x1
    return [x1.real if isinstance(x1, complex) else x1] if realRoot else [x1, x2, x3]


# 解一元四次方程
def math_ferrari_formula(a, b, c, d, e, realRoot=True) -> list:  # 费拉里公式
    # quartic equation of one unknown
    # general formula: a*x**4+b*x**3+cx**2+d*x+e=0
    if abs(a) < PL_A:  # compat cardano_formula
        return math_cardano_formula(b, c, d, e, realRoot)
    b1 = b/a
    c1 = c/a
    d1 = d/a
    e1 = e/a  # a1=1
    a = -1.0
    b = c1
    c = (4*e1-b1*d1)
    d = d1**2-e1*(4*c1-b1**2)
    yList = math_cardano_formula(a, b, c, d, False)
    # filtrate non-zero root
    y = yList[0] if abs(yList[0]) > PL_A else yList[1]
    a2 = (1/4*b1**2-c1+y)
    b2 = (1/2*b1*y-d1)
    c2 = (1/4*y**2-e1)
    b = b1/2+math_imag_sqrt(a2)
    c = y/2+math_sign(b2)*math_imag_sqrt(c2)
    rootC = []
    rootC.append((-b+math_imag_sqrt(b**2-4*c))/2)  # a=1
    rootC.append((-b-math_imag_sqrt(b**2-4*c))/2)
    b = b1/2-math_imag_sqrt(a2)
    c = y/2-math_sign(b2)*math_imag_sqrt(c2)
    rootC.append((-b+math_imag_sqrt(b**2-4*c))/2)
    rootC.append((-b-math_imag_sqrt(b**2-4*c))/2)
    rootR = []
    for i in rootC:  # filtrate real root
        # if abs(i.imag)<PL_A:rootR.append(i)
        if isinstance(i, complex) and abs(i.imag) < PL_E6:  # accuracy matters
            rootR.append(i.real)
        elif isinstance(i, float):
            rootR.append(i)
    return rootR if realRoot else rootC


def math_bisection_method(func: FunctionType, a: float, b: float, accu=PL_E6) -> float:  # 二分法求数值解
    # func(x)==0
    c = (a + b) / 2.0
    while(abs(func(c)) > accu):
        c = (a + b) / 2.0
        if (func(a) * func(c) < 0):
            b = c
        elif (func(b) * func(c) < 0):
            a = c
        else:
            break
    return c

# ------------------------------------------------------------------------------------------
# |                                         MATRIX                                         |
# ------------------------------------------------------------------------------------------


def math_adjust_matrix(matrix: list) -> list:  # 调整矩阵，使对角元素不为零
    n = len(matrix)
    matrix = copy.deepcopy(matrix)
    newMat = []
    for i in range(n):
        if abs(matrix[i][i]) > PL_A:
            newMat.append(matrix[i])
        else:
            for j in range(i+1, n):
                if abs(matrix[j][i]) > PL_A:
                    newMat.append(matrix[j])
                    matrix[j] = matrix[i]
                    break
    return newMat


def math_eye_matrix(n: int, a: float = 1) -> list:  # 二维对角矩阵
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(a)
            else:
                row.append(0.0)
        matrix.append(row)
    return matrix


def math_LU_factorization(U: list, b: list):  # 矩阵LU对角分解
    U = copy.deepcopy(U)
    b = copy.deepcopy(b)
    n = 5  # 5*5 matrix
    L = math_eye_matrix(n)
    for j in range(n-1):
        for i in range(j+1, n):
            L[i][j] = U[i][j]/U[j][j]
            for k in range(j, n):
                U[i][k] = U[i][k]-L[i][j]*U[j][k]
    # return (L,U)
    # solve Ly=b
    for i in range(1, n):
        sigma = 0
        for j in range(i):
            sigma = sigma+L[i][j]*b[j]
        b[i] = b[i]-sigma  # update b
    # solve Ux=b
    if abs(U[n-1][n-1]) < PL_A:
        raise TypeError('matrix rank error!')
    b[n-1] = b[n-1]/U[n-1][n-1]
    for i in range(n-1):
        k = n-(i+1)-1
        sigma = 0
        for j in range(k+1, n):
            sigma = sigma+U[k][j]*b[j]
        b[k] = (b[k]-sigma)/U[k][k]
    return b


# ------------------------------------------------------------------------------------------
# |                                         LINEAR                                         |
# ------------------------------------------------------------------------------------------


def get_coefficients_from_two_points(p1: GeVec3d, p2: GeVec3d) -> list:  # 平面直线两点式
    # (y2-y1)*x-(x2-x1)*y+(x2*y1-x1*y2)=0
    # the parameter equaltion form: P(t)=p1+t*(p2-p1)
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    A = y2-y1
    B = -(x2-x1)
    C = x2*y1-x1*y2
    return (A, B, C)
