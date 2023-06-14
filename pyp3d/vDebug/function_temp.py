from .pyp3d_function import *
# 临时全局函数
false = False
true = True
eps = 1e-6
_eps = -1e-6


def _is_all_fragment(val: list) -> bool:
    for iter in val:
        if isinstance(iter, Segment) or isinstance(iter, Arc) or isinstance(iter, SplineCurve) or \
                isinstance(iter, GeVec3d) or isinstance(iter, GeVec2d):
            continue
        else:
            return False
    return True


def loft_correspond_fragment(linesA: list, linesB: list) -> Loft:
    if len(linesA) != len(linesA) or not _is_all_fragment(linesA) or not _is_all_fragment(linesB):
        raise ValueError('loft_correspond_fragment parameter error!')
    # check coplanar
    secBot = Section(linesA)
    secTop = Section(linesB)
    return


def get_rand_point(is2D=True) -> GeVec3d:
    rg = 100
    if is2D:
        return GeVec3d(randint(-rg, rg), randint(-rg, rg))
    else:
        return GeVec3d(randint(-rg, rg), randint(-rg, rg), randint(-rg, rg))


def gen_rand_point(is2D=True) -> Point:
    rg = 100
    if is2D:
        return Point(randint(-rg, rg), randint(-rg, rg), 0)
    else:
        return Point(randint(-rg, rg), randint(-rg, rg), randint(-rg, rg))


def isPointInTriangle2D(point, trigon) -> bool:  # 2D
    # // using isLeft test
    # create_geometry(Sphere(point))
    p0 = trigon[0]
    p1 = trigon[1]
    p2 = trigon[2]
    ccw = (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y) > 0 #ccw Triangle
    if ccw:
        if ((p1.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p1.y - p0.y) < _eps):
            return false
        if ((p2.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p2.y - p0.y) > eps):
            return false
        if ((p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y) < _eps):
            return false
        return true
    else:
        if ((p1.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p1.y - p0.y) > eps):
            return false
        if ((p2.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p2.y - p0.y) < _eps):
            return false
        if ((p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y) > eps):
            return false
        return true


def isPointInTriangle(point: GeVec3d, trigon: list) -> bool:  # must coplanar
    # using isLeft test
    create_geometry(Sphere(point))
    normal = (trigon[1] - trigon[0]).cross(trigon[2] - trigon[0])
    if (((trigon[1] - trigon[0]).cross(point - trigon[0])).dot(normal) < _eps):  # bool isLeftA
        return false
    if (((trigon[2] - trigon[0]).cross(point - trigon[0])).dot(normal) > eps):  # bool isLeftB
        return false
    if (((trigon[2] - trigon[1]).cross(point - trigon[1])).dot(normal) < _eps):  # bool isLeftC
        return false
    return true


# 三角形最小包围圆 the Minimum Triangle Bounding Circle
def getTriangleBoundingCircle(trigon: list):
    vecA = trigon[1]-trigon[0]
    vecB = trigon[2]-trigon[0]
    vecC = trigon[2]-trigon[1]
    vecZ = vecA.cross(vecB)
    if (vecZ.norm2() > eps):
        p0 = trigon[0]
        p1 = trigon[1]
        p2 = trigon[2]
        mat = set_matrix_by_row_vectors(vecA, vecB, vecZ)
        p = inverse(mat)*GeVec3d(0.5*(p1.x*p1.x-p0.x*p0.x+p1.y*p1.y-p0.y*p0.y+p1.z*p1.z-p0.z*p0.z),
                                 0.5*(p2.x*p2.x-p0.x*p0.x+p2.y*p2.y -
                                      p0.y*p0.y+p2.z*p2.z-p0.z*p0.z),
                                 vecZ.dot(p0))
        if (isPointInTriangle(p, trigon)):  # is acute angle
            return (p, (p-p0).norm())
    # illegal and obtuse angle
    a = vecA.norm2()
    b = vecB.norm2()
    c = vecC.norm2()
    if (a > b and a > c):
        return (0.5*(trigon[0]+trigon[1]), 0.5*sqrt(a))
    elif (b > a and b > c):
        return (0.5*(trigon[0]+trigon[2]), 0.5*sqrt(b))
    else:
        return (0.5*(trigon[1]+trigon[2]), 0.5*sqrt(c))
