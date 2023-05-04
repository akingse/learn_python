import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..//"))
from pyp3d import *


def sweep_parallel(sec: Section, line: Line):
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
        P = paraList[-1]
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

    # B = polyline[i+1]
    # C = polyline[i+2]
    # P = paraList[-1]
    # k = -dot(P-C, C-B)/dot(C-B, C-B)
    # pLast = P+k*(C-B)
    # paraList.append(P+k*(C-B))
    matS = get_matrix_from_three_points(
        [polyline[0], polyline[1], pStart], False)
    matE = get_matrix_from_three_points(
        [polyline[-1], 2*polyline[-1]-polyline[-2], paraList[-1]], False)
    pLast = (matE*inverse_std(matS))*pStart
    paraList.append(pLast)

    geo = sweep_stere(sec, Line(paraList))
    return geo
