from .pyp3d_function import *
import math
import numpy as np
# 临时全局函数
false = False
true = True
eps = 1.192092896e-07
_eps = -1.192092896e-07
DBL_MAX = 1.7976931348623157e+308
# Nodes number in one element cube
#    7 ____________ 6
#    /            /|    ^ z
#   /___________ / |    |     ^  y
# 4|          5 |  |    |    /
#  |            |  |    |   /
#  |  3         |  |2   |  /
#  |            | /     | /
#  |____________|/       ----------> x
# 0           1


def create_bounding_box(box):
    min=box[0]# GeVec3d
    max=box[1]# GeVec3d
    create_geometry(trans(min)*scale(max-min)*Cube())


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


def get_rand_point(demi=2) -> GeVec3d:
    rg = 100
    if demi == 2:
        return GeVec3d(randint(-rg, rg), randint(-rg, rg))
    elif demi == 3:
        return GeVec3d(randint(-rg, rg), randint(-rg, rg), randint(-rg, rg))


def get_rand_box() -> list:
    rg = 100
    # _min = get_rand_point(2) #
    _min=get_rand_point(3) #GeVec3d(randint(-rg, rg), randint(-rg, rg), randint(-rg, rg))
    return [_min, _min+GeVec3d(randint(rg/2, rg), randint(rg/2, rg), randint(rg/2, rg))]


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
    # ccw = (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * \
    #     (p1.y - p0.y) > 0  # ccw Triangle
    # if ccw:
    #     if ((p1.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p1.y - p0.y) < _eps):
    #         return false
    #     if ((p2.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p2.y - p0.y) > eps):
    #         return false
    #     if ((p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y) < _eps):
    #         return false
    #     return true
    # else:
    #     if ((p1.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p1.y - p0.y) > eps):
    #         return false
    #     if ((p2.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p2.y - p0.y) < _eps):
    #         return false
    #     if ((p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y) > eps):
    #         return false
    #     return true

    # if (0.0 < (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)):
    #     return not (((p1.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p1.y - p0.y) < 0.0) or  # bool isLeftA
    #             ((p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y) < 0.0) or # bool isLeftB
    #             ((p0.x - p2.x) * (point.y - p2.y) - (point.x - p2.x) * (p0.y - p2.y) < 0.0))  # bool isLeftC
    # else:
    #     return not (((p1.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p1.y - p0.y) > 0.0) or  # bool isLeftA
    #             ((p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y) > 0.0) or # bool isLeftB
    #             ((p0.x - p2.x) * (point.y - p2.y) - (point.x - p2.x) * (p0.y - p2.y) > 0.0))  # bool isLeftC

    axisz = (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)
    return (0.0 <= axisz*((p1.x - p0.x) * (point.y - p0.y) - (point.x - p0.x) * (p1.y - p0.y))) and \
        (0.0 <= axisz*((p2.x - p1.x) * (point.y - p1.y) - (point.x - p1.x) * (p2.y - p1.y))) and \
        (0.0 <= axisz*((p0.x - p2.x) * (point.y - p2.y) - (point.x - p2.x) * (p0.y - p2.y)))


def isPointInTriangle(point: GeVec3d, trigon: list) -> bool:  # must coplanar
    # using isLeft test
    if (point[0] < min(min(trigon[0][0], trigon[1][0]), trigon[2][0]) or
        point[0] > max(max(trigon[0][0], trigon[1][0]), trigon[2][0]) or
        point[1] < min(min(trigon[0][1], trigon[1][1]), trigon[2][1]) or
        point[1] > max(max(trigon[0][1], trigon[1][1]), trigon[2][1]) or
        point[2] < min(min(trigon[0][2], trigon[1][2]), trigon[2][2]) or
        point[2] > max(max(trigon[0][2], trigon[1][2]), trigon[2][2])):
        return False # using absolute zero
    vecZ = (trigon[1] - trigon[0]).cross(trigon[2] - trigon[0]).normalized()
    isNorm=False #True #
    if isNorm:
    # big number must normalized, otherwise point on edge will error
        return _eps < ((trigon[1] - trigon[0]).normalized().cross((point - trigon[0]).normalized())).dot(vecZ) and \
            _eps < ((trigon[2] - trigon[1]).normalized().cross((point - trigon[1]).normalized())).dot(vecZ) and \
            _eps < ((trigon[0] - trigon[2]).normalized().cross((point - trigon[2]).normalized())).dot(vecZ)
    else:
        return not ((trigon[1] - trigon[0]).cross( point - trigon[0]).dot(vecZ) < _eps or
                    (trigon[2] - trigon[1]).cross( point - trigon[1]).dot(vecZ) < _eps or
                    (trigon[0] - trigon[2]).cross( point - trigon[2]).dot(vecZ) < _eps)

def printTriangle(trigon):
    print_vector(trigon[0])
    print_vector(trigon[1])
    print_vector(trigon[2])
    print('--------------------------')


def printTrianglePair(triA, triB):
    pre = 'triB_2 = Vec3'
    print_vector(triA[0])
    print_vector(triA[1])
    print_vector(triA[2])
    print_vector(triB[0])
    print_vector(triB[1])
    print_vector(triB[2])
    print('--------------------------')

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


def isTwoSegmentsIntersect(segmA, segmB):
    if (max([segmA[0][0], segmA[1][0]]) < min([segmB[0][0], segmB[1][0]]) or
        min([segmA[0][0], segmA[1][0]]) > max([segmB[0][0], segmB[1][0]]) or
        max([segmA[0][1], segmA[1][1]]) < min([segmB[0][1], segmB[1][1]]) or
        min([segmA[0][1], segmA[1][1]]) > max([segmB[0][1], segmB[1][1]]) or
        max([segmA[0][2], segmA[1][2]]) < min([segmB[0][2], segmB[1][2]]) or
            min([segmA[0][2], segmA[1][2]]) > max([segmB[0][2], segmB[1][2]])):
        return False
    return not (
        (segmB[0] - segmA[0]).cross(segmA[1] - segmA[0]).dot((segmA[1] - segmA[0]).cross(segmB[1] - segmA[0])) < _eps or
        (segmA[0] - segmB[0]).cross(segmB[1] - segmB[0]).dot((segmB[1] - segmB[0]).cross(segmA[1] - segmB[0])) < _eps)


def isTwoTrianglesIntersection2D(triA, triB):
    pA0 = triA[0]
    pA1 = triA[1]
    pA2 = triA[2]
    pB0 = triB[0]
    pB1 = triB[1]
    pB2 = triB[2]
    vecA0 = triA[1] - triA[0]
    vecA1 = triA[2] - triA[1]
    vecA2 = triA[0] - triA[2]
    axisA0 = Vec3(-vecA0.y, vecA0.x)
    axisA1 = Vec3(-vecA1.y, vecA1.x)
    axisA2 = Vec3(-vecA2.y, vecA2.x)
    dotA0 = axisA0.dot(pA0)
    dotA1 = axisA0.dot(pA1)
    dotA2 = axisA0.dot(pA2)
    dotB0 = axisA0.dot(pB0)
    dotB1 = axisA0.dot(pB1)
    dotB2 = axisA0.dot(pB2)
    # show_points_line([Vec3(), axisA0])
    return


def isTwoTrianglesIntersectSAT(triA, triB) -> bool:
    edgesA = [triA[1] - triA[0], triA[2] - triA[1], triA[0] - triA[2]]
    edgesB = [triB[1] - triB[0], triB[2] - triB[1], triB[0] - triB[2]]
    # isNorm = False #unitize every edge
    # if isNorm:
    #     axes = [(edgesA[0].cross(edgesB[0])).normalized(),
    #             (edgesA[0].cross(edgesB[1])).normalized(),
    #             (edgesA[0].cross(edgesB[2])).normalized(),
    #             (edgesA[1].cross(edgesB[0])).normalized(),
    #             (edgesA[1].cross(edgesB[1])).normalized(),
    #             (edgesA[1].cross(edgesB[2])).normalized(),
    #             (edgesA[2].cross(edgesB[0])).normalized(),
    #             (edgesA[2].cross(edgesB[1])).normalized(),
    #             (edgesA[2].cross(edgesB[2])).normalized(),
    #             (edgesA[0]).normalized(),
    #             (edgesA[1]).normalized(),
    #             (edgesA[2]).normalized(),
    #             (edgesB[0]).normalized(),
    #             (edgesB[1]).normalized(),
    #             (edgesB[2]).normalized()]
    normalA = edgesA[0].cross(edgesA[1])
    normalB = edgesB[0].cross(edgesB[1])
    if (normalA.cross(normalB).normalized().norm()<eps): #isZero()
        axes = [edgesA[0].cross(edgesA[1]),
                # edgesA[0],
                # edgesA[1],
                # edgesA[2],
                # edgesB[0],
                # edgesB[1],
                # edgesB[2],
                # crossAB
                normalA.cross(edgesA[0]),
                normalA.cross(edgesA[1]),
                normalA.cross(edgesA[2]),
                normalB.cross(edgesB[0]),
                normalB.cross(edgesB[1]),
                normalB.cross(edgesB[2])]
    else:
        axes = [
            # edgesA[0],
            # edgesA[1],
            # edgesA[2],
            # edgesB[0],
            # edgesB[1],
            # edgesB[2],
            edgesA[0].cross(edgesA[1]),
            edgesB[0].cross(edgesB[1]),
            # crossAB
            edgesA[0].cross(edgesB[0]),
            edgesA[0].cross(edgesB[1]),
            edgesA[0].cross(edgesB[2]),
            edgesA[1].cross(edgesB[0]),
            edgesA[1].cross(edgesB[1]),
            edgesA[1].cross(edgesB[2]),
            edgesA[2].cross(edgesB[0]),
            edgesA[2].cross(edgesB[1]),
            edgesA[2].cross(edgesB[2])]
    # for axis in axes:
    #     create_geometry(Line(Vec3(),axis).colorRand())
    # show_points_line([triA[0],triA[1]])
    # show_points_line([triB[0],triB[1]])
    # show_points_line([triB[0],triB[0]+edgesA[0]])
    # create_geometry(Line(Vec3(),axes[0]).colorRand())
    for axis in axes:
        dotA0 = triA[0].dot(axis)
        dotA1 = triA[1].dot(axis)
        dotA2 = triA[2].dot(axis)
        dotB0 = triB[0].dot(axis)
        dotB1 = triB[1].dot(axis)
        dotB2 = triB[2].dot(axis)
        minA = min(min(dotA0, dotA1), dotA2)
        maxA = max(max(dotA0, dotA1), dotA2)
        minB = min(min(dotB0, dotB1), dotB2)
        maxB = max(max(dotB0, dotB1), dotB2)
        if maxA < minB or maxB < minA:
            # if maxA + eps < minB or maxB + eps < minA:
            return False
    return True


def isTwoTrianglesBoundingBoxIntersect(triA, triB, tolerance=0.0):
    if (max(triB[0].x, triB[1].x, triB[2].x) <
            min(triA[0].x, triA[1].x, triA[2].x) - tolerance):
        return False
    if (max(triA[0].x, triA[1].x, triA[2].x) + tolerance <
            min(triB[0].x, triB[1].x, triB[2].x)):
        return False
    if (max(triB[0].y, triB[1].y, triB[2].y) <
            min(triA[0].y, triA[1].y, triA[2].y) - tolerance):
        return False
    if (max(triA[0].y, triA[1].y, triA[2].y) + tolerance <
            min(triB[0].y, triB[1].y, triB[2].y)):
        return False
    if (max(triB[0].z, triB[1].z, triB[2].z) <
            min(triA[0].z, triA[1].z, triA[2].z) - tolerance):
        return False
    if (max(triA[0].z, triA[1].z, triA[2].z) + tolerance <
            min(triB[0].z, triB[1].z, triB[2].z)):
        return False
    return True


def isSegmentAndTriangleIntersctSAT(segment, trigon):
    vecZ = (trigon[1] - trigon[0]).cross(trigon[2] - trigon[0])
    if (abs(vecZ.dot(segment[0] - trigon[0])) < eps and abs(vecZ.dot(segment[1] - trigon[0])) < eps):  # the coplanar
        axes = [vecZ.cross(segment[1] - segment[0]),
                vecZ.cross(trigon[1] - trigon[0]),
                vecZ.cross(trigon[2] - trigon[1]),
                vecZ.cross(trigon[0] - trigon[2])]
    else:
        edges = [trigon[1] - trigon[0], trigon[2] -
                 trigon[1], trigon[0] - trigon[2]]
        vecSeg = segment[1] - segment[0]
        axes = [edges[0],
                edges[1],
                edges[2],
                vecSeg,
                vecSeg.cross(edges[0]),
                vecSeg.cross(edges[1]),
                vecSeg.cross(edges[2])]
    for axis in axes:
        dotA0 = trigon[0].dot(axis)
        dotA1 = trigon[1].dot(axis)
        dotA2 = trigon[2].dot(axis)
        dotB0 = segment[0].dot(axis)
        dotB1 = segment[1].dot(axis)
        minA = min(min(dotA0, dotA1), dotA2)
        maxA = max(max(dotA0, dotA1), dotA2)
        minB = min(dotB0, dotB1)
        maxB = max(dotB0, dotB1)
        if maxA < minB or maxB < minA:
            return False
    return True


def isTriangleAndBoundingBoxIntersect(trigon: list, box: list) -> bool:
    min = box[0]
    max = box[1]
    # is point in box
    p0 = trigon[0]
    p1 = trigon[1]
    p2 = trigon[2]
    if (min.x <= p0.x and min.y <= p0.y and min.z <= p0.z and
            max.x >= p0.x and max.y >= p0.y and max.z >= p0.z):
        return true  # contains vertex
    if (min.x <= p1.x and min.y <= p1.y and min.z <= p1.z and
            max.x >= p1.x and max.y >= p1.y and max.z >= p1.z):
        return true  # contains vertex
    if (min.x <= p2.x and min.y <= p2.y and min.z <= p2.z and
            max.x >= p2.x and max.y >= p2.y and max.z >= p2.z):
        return true  # contains vertex
    pO0 = p0-min
    pO1 = p1-min
    pO2 = p2-min
    vertex = max-min
    # genarate 12 triangles
    triTwelve = [[Vec3(0, 0, 0), Vec3(vertex.x, 0, 0), Vec3(vertex.x, vertex.y, 0)],
                 [Vec3(0, 0, 0), Vec3(0, vertex.y, 0),
                  Vec3(vertex.x, vertex.y, 0)],
                 [Vec3(0, 0, vertex.z), Vec3(vertex.x, 0, vertex.z), vertex],
                 [Vec3(0, 0, vertex.z), Vec3(0, vertex.y, vertex.z), vertex],
                 [Vec3(0, 0, 0), Vec3(vertex.x, 0, 0),
                  Vec3(vertex.x, 0, vertex.z)],
                 [Vec3(0, 0, 0), Vec3(0, 0, vertex.z),
                  Vec3(vertex.x, 0, vertex.z)],
                 [Vec3(0, vertex.y, 0), Vec3(vertex.x, vertex.y, 0), vertex],
                 [Vec3(0, vertex.y, 0), Vec3(0, vertex.y, vertex.z), vertex],
                 [Vec3(0, 0, 0), Vec3(0, vertex.y, 0),
                  Vec3(0, vertex.y, vertex.z)],
                 [Vec3(0, 0, 0), Vec3(0, 0, vertex.z),
                  Vec3(0, vertex.y, vertex.z)],
                 [Vec3(vertex.x, 0, 0), Vec3(vertex.x, vertex.y, 0), vertex],
                 [Vec3(vertex.x, 0, 0), Vec3(vertex.x, 0, vertex.z), vertex]]
    for iter in triTwelve:
        if isTwoTrianglesIntersectSAT([pO0, pO1, pO2], iter):
            return true
    return false


def isTriangleAndBoundingBoxIntersectSAT(trigon, box):
    p0, p1, p2 = trigon
    _min, _max = box[0], box[1]
    if (max(p0.x, p1.x, p2.x) < _min.x or
        min(p0.x, p1.x, p2.x) > _max.x or
        max(p0.y, p1.y, p2.y) < _min.y or
        min(p0.y, p1.y, p2.y) > _max.y or
        max(p0.z, p1.z, p2.z) < _min.z or
        min(p0.z, p1.z, p2.z) > _max.z):
        return False
    edges = [p1 - p0, p2 - p1, p0 - p2]
    coords = [GeVec3d(1, 0, 0), GeVec3d(0, 1, 0), GeVec3d(0, 0, 1)]
    axes = [
        coords[0],
        coords[1],
        coords[2],
        # edges[0], # edge can remove
        # edges[1],
        # edges[2],
        edges[0].cross(edges[1]),
        coords[0].cross(edges[0]),
        coords[0].cross(edges[1]),
        coords[0].cross(edges[2]),
        coords[1].cross(edges[0]),
        coords[1].cross(edges[1]),
        coords[1].cross(edges[2]),
        coords[2].cross(edges[0]),
        coords[2].cross(edges[1]),
        coords[2].cross(edges[2])
    ]
    origin = box[0]
    vertex = box[1]-box[0]
    vertexes = [
        GeVec3d(0, 0, 0),
        GeVec3d(vertex.x, 0, 0),
        GeVec3d(vertex.x, vertex.y, 0),
        GeVec3d(0, vertex.y, 0),
        GeVec3d(0, 0, vertex.z),
        GeVec3d(vertex.x, 0, vertex.z),
        GeVec3d(vertex.x, vertex.y, vertex.z),
        GeVec3d(0, vertex.y, vertex.z)
    ]
    for axis in axes:
        minA = DBL_MAX
        maxA = -DBL_MAX
        minB = DBL_MAX
        maxB = -DBL_MAX
        for vertex in trigon:
            projection = (vertex - origin).dot(axis)
            minA = min(minA, projection)
            maxA = max(maxA, projection)
        for vertex in vertexes:
            projection = vertex.dot(axis)
            minB = min(minB, projection)
            maxB = max(maxB, projection)
        if maxA < minB or maxB < minA:
            return False
    return True


def isTwoTrianglesBoundingBoxIntersect(triA, triB, tolerance):
    xminA = min(triA[0].x, triA[1].x, triA[2].x) - tolerance
    xmaxA = max(triA[0].x, triA[1].x, triA[2].x) + tolerance
    yminA = min(triA[0].y, triA[1].y, triA[2].y) - tolerance
    ymaxA = max(triA[0].y, triA[1].y, triA[2].y) + tolerance
    zminA = min(triA[0].z, triA[1].z, triA[2].z) - tolerance
    zmaxA = max(triA[0].z, triA[1].z, triA[2].z) + tolerance
    xminB = min(triB[0].x, triB[1].x, triB[2].x)
    xmaxB = max(triB[0].x, triB[1].x, triB[2].x)
    yminB = min(triB[0].y, triB[1].y, triB[2].y)
    ymaxB = max(triB[0].y, triB[1].y, triB[2].y)
    zminB = min(triB[0].z, triB[1].z, triB[2].z)
    zmaxB = max(triB[0].z, triB[1].z, triB[2].z)
    # create boundingbox
    create_bounding_box(Vec3(xminA, yminA, zminA), Vec3(xmaxA, ymaxA, zmaxA))
    create_bounding_box(Vec3(xminB, yminB, zminB), Vec3(xmaxB, ymaxB, zmaxB))
    return not (xminA > xmaxB or yminA > ymaxB or zminA > zmaxB
                or xminB > xmaxA or yminB > ymaxA or zminB > zmaxA)
    # return xminA <= xmaxB and yminA <= ymaxB and zminA <= zmaxB  \
    #     and xminB <= xmaxA and yminB <= ymaxA and zminB <= zmaxA
    # if xmaxA < xminB or xminA > xmaxB:
    #     return false
    # if ymaxA < yminB or yminA > ymaxB:
    #     return false
    # if zmaxA < zminB or zminA > zmaxB:
    #     return false
    # return True


# 测试 isTwoTrianglesIntersection1
def TrianglesIntersection_part1(triL, triR):  # 线段在平面两侧
    veczL = (triL[1] - triL[0]).cross(triL[2] - triL[0])
    acrossR2L_A = (veczL.dot(triR[0] - triL[0])) * \
        (veczL.dot(triR[1] - triL[0])) < eps  # 包括点在平面上
    acrossR2L_B = (veczL.dot(triR[1] - triL[0])) * \
        (veczL.dot(triR[2] - triL[0])) < eps
    acrossR2L_C = (veczL.dot(triR[2] - triL[0])) * \
        (veczL.dot(triR[0] - triL[0])) < eps
    if not acrossR2L_A and not acrossR2L_B and not acrossR2L_C:
        return False
    veczR = (triR[1] - triR[0]).cross(triR[2] - triR[0])
    acrossL2R_A = (veczR.dot(triL[0] - triR[0])) * \
        (veczR.dot(triL[1] - triR[0])) < eps
    acrossL2R_B = (veczR.dot(triL[1] - triR[0])) * \
        (veczR.dot(triL[2] - triR[0])) < eps
    acrossL2R_C = (veczR.dot(triL[2] - triR[0])) * \
        (veczR.dot(triL[0] - triR[0])) < eps
    if not acrossL2R_A and not acrossL2R_B and not acrossL2R_C:
        return False

    return True


def TrianglesIntersection_part1_(triL, triR, mat=g_matrixE):
    res0 = TrianglesIntersection_part1(mat*triL, mat*triR)
    res1 = TrianglesIntersection_part1(mat*triR, mat*triL)
    if (res0 != res1):
        raise ValueError("-------")
    return res0


def is_straddling_test(segm, edge) -> bool:
    # 如果两线段相交，则两线段必然相互跨立对方.若A1A2跨立B1B2，则矢量(A1-B1) 和(A2-B1)位于矢量(B2-B1)的两侧
    # (A1-B1) × (B2-B1) * (B2-B1) × (A2-A1) >= 0
    # (B1-A1) × (A2-A1) * (A2-A1) × (B2-A1) >= 0

    isStra = (edge[0]-segm[0]).cross(segm[1]-segm[0]).dot(
             (segm[1]-segm[0]).cross(edge[1]-segm[0])) > _eps
    if (edge[0]-segm[0]).cross(segm[1]-segm[0]).dot(
            (segm[1]-segm[0]).cross(edge[1]-segm[0])) < _eps:
        return false
    if (segm[0]-edge[0]).cross(edge[1]-edge[0]).dot(
            (edge[1]-edge[0]).cross(segm[1]-edge[0])) < _eps:
        return false
    return true
    # return not((edge[0]-segm[0]).cross(segm[1]-segm[0]).dot((segm[1]-segm[0]).cross(edge[1]-segm[0])) < _eps or
    #            (segm[0]-edge[0]).cross(edge[1]-edge[0]).dot((edge[1]-edge[0]).cross(segm[1]-edge[0])) < _eps)


def isPointRayAcrossTriangle(point, trigon):
    if (point.z > max(trigon[0].z, trigon[1].z, trigon[2].z) or
        point.x > max(trigon[0].x, trigon[1].x, trigon[2].x) or
        point.x < min(trigon[0].x, trigon[1].x, trigon[2].x) or
        point.y > max(trigon[0].y, trigon[1].y, trigon[2].y) or
            point.y < min(trigon[0].y, trigon[1].y, trigon[2].y)):
        return False
    inf = 3.402823466e+38
    ray = GeVec3d(point.x, point.y, inf)
    axisZ = GeVec3d(0, 0, 1)
    edges = [trigon[1] - trigon[0],
             trigon[2] - trigon[1],
             trigon[0] - trigon[2]]
    axes = [axisZ.cross(edges[0]),
            axisZ.cross(edges[1]),
            axisZ.cross(edges[2]),
            axisZ,
            edges[0],
            edges[1],
            edges[2]]
    for axis in axes:
        dotA0 = axis.dot(trigon[0])
        dotA1 = axis.dot(trigon[1])
        dotA2 = axis.dot(trigon[2])
        minTri = min(min(dotA0, dotA1), dotA2)
        maxTri = max(max(dotA0, dotA1), dotA2)
        minRay = min(axis.dot(point), axis.dot(ray))
        maxRay = max(axis.dot(point), axis.dot(ray))
        if maxTri < minRay or maxRay < minTri:
            return False
    return True


def Polyhedron4():
    polyface = Polyface('')
    polyface.vertexList = [Vec3(0, 0, 0), Vec3(
        1, 0, 0), Vec3(0.5, 1, 0), Vec3(0.5, 0.5, 1)]
    polyface.faceList = [int(1), int(2), int(3), int(0),
                         int(1), int(2), int(4), int(0),
                         int(2), int(3), int(4), int(0),
                         int(3), int(1), int(4), int(0)]
    return polyface


def Polyhedron5():
    polyface = Polyface('')
    polyface.vertexList = [Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(
        1, 1, 0), Vec3(0, 1, 0), Vec3(0.5, 0.5, 1)]
    polyface.faceList = [int(1), int(2), int(3), int(4), int(0),
                         int(1), int(2), int(5), int(0),
                         int(2), int(3), int(5), int(0),
                         int(3), int(4), int(5), int(0),
                         int(4), int(1), int(5), int(0)]
    return polyface


def _getIntersectOfSegmentAndPlaneINF(segment,  plane, vecSeg) -> float:
    normal = (plane[1] - plane[0]).cross(plane[2] - plane[1])
    vecSeg[0] = segment[1] - segment[0]
    if (fabs(vecSeg[0].normalized().dot(normal.normalized())) < eps):
        return DBL_MAX if(fabs((segment[0] - plane[0]).normalized().dot(normal.normalized())) < eps) else -DBL_MAX
    return (plane[0] - segment[0]).dot(normal) / vecSeg[0].dot(normal)

def getIntersectOfSegmentAndPlaneINF(segment,  plane) -> GeVec3d:
    normal = (plane[1] - plane[0]).cross(plane[2] - plane[1])
    vecSeg=[g_axisNaN]
    vecSeg[0] = segment[1] - segment[0]
    if (fabs(vecSeg[0].normalized().dot(normal.normalized())) < eps): #parallel
        return g_axisNaN #DBL_MAX if(fabs((segment[0] - plane[0]).dot(normal)) < eps) else -DBL_MAX
    k = (plane[0] - segment[0]).dot(normal) / vecSeg[0].dot(normal)
    local = segment[0] + k * vecSeg[0]
    return local

def isTwoIntersectTrianglesCoplanar(triA,triB)->bool: #must intersect
    normalA = (triA[1] - triA[0]).cross(triA[2] - triA[0])#.normalized()
    normalB = (triB[1] - triB[0]).cross(triB[2] - triB[0])#.normalized()
    # croPro=normalA.cross(normalB)
    return normalA.cross(normalB).normalized().isZero(eps)

def _getPointOfTwoIntersectSegments(segmA,  segmB) -> float:
    normal = (segmB[0] - segmB[1]).cross(segmA[1]-segmA[0])
    if (normal.isZero()):
        return DBL_MAX
    return (segmA[0] - segmB[0]).cross(segmA[0] - segmB[1]).norm() / normal.norm()


def getTwoTrianglesIntersectPoints(triA, triB):
    res = [g_axisNaN, g_axisNaN]
    # if not isTwoTrianglesIntersectSAT(triA, triB):
    #     return res
    edgesA = [[triA[0], triA[1]],
              [triA[1], triA[2]],
              [triA[2], triA[0]]]
    edgesB = [[triB[0], triB[1]],
              [triB[1], triB[2]],
              [triB[2], triB[0]]]
    count = 0
    vecSeg = [g_axisNaN]
    for edgeA in edgesA:
        k = _getIntersectOfSegmentAndPlaneINF(edgeA, triB, vecSeg)
        if k == DBL_MAX:  # coplanar
            if isPointInTriangle(edgeA[0], triB) and isPointInTriangle(edgeA[1], triB):
                return edgeA
            for edgeB in edgesB:
                if not isTwoSegmentsIntersect(edgeA, edgeB):
                    continue
                k2 = _getPointOfTwoIntersectSegments(edgeA, edgeB)
                if k2 == DBL_MAX:  # collinear
                    if (edgeA[0] - edgeB[0]).dot(edgeA[0] - edgeB[1]) <= 0 and (edgeA[1] - edgeB[0]).dot(edgeA[1] - edgeB[1]) <= 0: 
                        res =edgeA
                    elif (edgeB[0] - edgeA[0]).dot(edgeB[0] - edgeA[1]) <= 0 and (edgeB[1] - edgeA[0]).dot(edgeB[1] - edgeA[1]) <= 0 :
                        res =edgeB
                    else:
                        res[0] = edgeA[0] if (
                            edgeA[0] - edgeB[0]).dot(edgeA[0] - edgeB[1]) <= 0 else edgeA[1]
                        res[1] = edgeB[0] if (
                            edgeB[0] - edgeA[0]).dot(edgeB[0] - edgeA[1]) <= 0 else edgeB[1]
                    return res
                res[count] = edgeA[0] + k2 * vecSeg[0]
                count += 1
                if count == 2:
                    return res
        elif 0 <= k <= 1:
            local = edgeA[0] + k * vecSeg[0]
            if not isPointInTriangle(local, triB):
                continue
            res[count] = local
            count += 1
            if count == 2:
                return res
    for edgeB in edgesB:
        k = _getIntersectOfSegmentAndPlaneINF(edgeB, triA, vecSeg)
        if k == DBL_MAX:  # coplanar
            if isPointInTriangle(edgeB[0], triA) and isPointInTriangle(edgeB[1], triA):
                return edgeB
            for edgeA in edgesA:
                if not isTwoSegmentsIntersect(edgeB, edgeA):
                    continue
                k2 = _getPointOfTwoIntersectSegments(edgeB, edgeA)
                if k2 == DBL_MAX:  # collinear
                    if (edgeA[0] - edgeB[0]).dot(edgeA[0] - edgeB[1]) <= 0 and (edgeA[1] - edgeB[0]).dot(edgeA[1] - edgeB[1]) <= 0: 
                        res =edgeA
                    elif (edgeB[0] - edgeA[0]).dot(edgeB[0] - edgeA[1]) <= 0 and (edgeB[1] - edgeA[0]).dot(edgeB[1] - edgeA[1]) <= 0 :
                        res =edgeB
                    else:
                        res[0] = edgeA[0] if (
                            edgeA[0] - edgeB[0]).dot(edgeA[0] - edgeB[1]) <= 0 else edgeA[1]
                        res[1] = edgeB[0] if (
                            edgeB[0] - edgeA[0]).dot(edgeB[0] - edgeA[1]) <= 0 else edgeB[1]
                    return res
                res[count] = edgeB[0] + k2 * vecSeg[0]
                count += 1
                if count == 2:
                    return res
        elif 0 <= k <= 1:
            local = edgeB[0] + k * vecSeg[0]
            if not isPointInTriangle(local, triA):
                continue
            res[count] = local
            count += 1
            if count == 2:
                return res
    return res
