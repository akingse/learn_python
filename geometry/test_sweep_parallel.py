import sys
import os
# mypath = r"C:\Users\Aking\Documents\WXWork\1688856575247594\Cache\File\2022-06\Release (1)\PythonScript\python-3.7.9-embed-amd64\Lib\site-packages"
sys.path.append(os.path.join(os.path.dirname(__file__), "..//"))
from pyp3d import *


def getLoftFromTwoArcs(angleXt, angleYt, angleXb=0, angleYb=0):
    mat = GeTransform([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [tan(angleXt), tan(angleYt), 1, 0]])

    axisXt = scale(100)*roty(angleXt)*scale(1/cos(angleXt))*g_axisX
    axisYt = scale(100)*rotx(angleYt)*scale(1/cos(angleYt))*g_axisY
    axisXb = scale(100)*roty(angleXb)*scale(1/cos(angleXb))*g_axisX
    axisYb = scale(100)*rotx(-angleYb)*scale(1/cos(-angleYb))*g_axisY
    matT = transz(50)*set_matrix_by_column_vectors(axisXt,
                                                   axisYt, cross(axisXt, axisYt))
    matB = transz(-100)*set_matrix_by_column_vectors(axisXb, axisYb, g_axisZ)
    # cone = Loft(matT*arcT, matB*arcB)
    disT = get_discrete_points_from_section(matT*arcT, 1000)
    disB = get_discrete_points_from_section(matB*arcB, 1000)
    cone = Loft(Section(disT), Section(disB))
    cone.smooth = True
    # test start
    arcT = matT*Arc()
    arcB = matB*Arc()
    pT = arcT.pointStart
    B = arcB.pointStart


get_distance_of_point_line
# 平行约束，会不会在某些情况下不存在线满足约束
# /--| 可能会导致-消失，暂未处理，可能要消去合并点


def _sweep_parallel(sec: Section, line: Line):

    # k = -dot(B-A, A-P)/dot(B-A, B-A)
    # D = A+k*(B-A)
    # The distance from the point to the line
    # return norm(A-P+dot(A-B, A-P)/dot(B-A, B-A)*(B-A)) #
    polyline = get_nested_parts_from_line(line)
    if not is_all_vec3(polyline) or len(polyline) < 3:
        raise TypeError("points number error!")
    pStart = get_first_point_on_section(sec)
    paraList = [pStart]
    # segment remove coincident
    # calculate the parallel line of polyline //the end point on the same plane

    # using 2D
    # xa, ya, za = polyline[0].x, polyline[0].y, polyline[0].z
    # xb, yb, zb = polyline[0].x, polyline[0].y, polyline[0].z
    # xc, yc, zc = polyline[0].x, polyline[0].y, polyline[0].z
    # xp, yp, zp = pStart.x, pStart.y, pStart.z

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
        # if (inverse_std(mat)*P).y >= 0:  # in angle, same quadrant side
        #     sign = -1.0
        # else:
        #     sign = 1.0
        sign = math_sign((inverse_std(mat)*P).y)
    # dot((C-B), (B-P))  # (C-B)*(B-P)
    # dot((C-B), (B-A))  # (C-B)*(B-A)
    # dot((C-B), (C-B))  # (C-B)*(C-B)
    # j = dot((C-B)*(B-A))/dot((C-B)*(C-B))*k - \
    #     dot((C-B)*(B-P))/dot((C-B)*(C-B))
    # d = (B-P)+k*(B-A)-j*(C-B)
    # d = (B-P)+k*(B-A)-k*dot((C-B)*(B-A))/dot((C-B)*(C-B))*(C-B) +\
    #     dot((C-B)*(B-P))/dot((C-B)*(C-B))*(C-B)
    # d^2=(m*k+n)^2
    # 矢量乘满足结合律，不满足交换律，故不能化简
        m = (A-B)+dot((C-B), (B-A))/dot((C-B), (C-B))*(C-B)
        n = (B-P)-dot((C-B), (B-P))/dot((C-B), (C-B))*(C-B)
        if norm(m) < PL_A:  # while three points collinear
            k = -dot(P-B, B-A)/dot(B-A, B-A)
        else:
            k = (-2*dot(m, n)-sign*sqrt(4*dot(m, n)*dot(m, n)-4 *
                                        dot(m, m)*(dot(n, n)-d * d)))/(2*dot(m, m))
        if k < 0:
            raise TypeError("vector direction error!")
        pIter = P+k*(B-A)
        paraList.append(pIter)
    # A = dot(m, m)  # m*m
    # B = 2*dot(m, n)  # 2*m*n
    # C = dot(n, n)-d * d  # n*n-d*d
    # k = (-B+sqrt(B*B-4*A*C))/(2*A)
    B = polyline[i+1]
    C = polyline[i+2]
    P = paraList[-1]
    # 规则1 与末端点保持共面
    k = -dot(P-C, C-B)/dot(C-B, C-B)
    pLast = P+k*(C-B)
    # paraList.append(P+k*(C-B))
    # 规则2 与第一矢量保持平行
    matS = get_matrix_from_three_points(
        [polyline[0], polyline[1], pStart], False)
    matE = get_matrix_from_three_points(
        [polyline[-1], 2*polyline[-1]-polyline[-2], paraList[-1]], False)
    # matS = get_matrix_from_two_vectors(
    #     polyline[1]-polyline[0], polyline[0]-pStart)
    # matE = get_matrix_from_two_vectors(
    #     polyline[-1]-polyline[-2], polyline[-1]-paraList[-1])
    # show_coordinate_system(matS)
    # show_coordinate_system(matE)
    pEnd = (matE*inverse_std(matS))*pStart
    paraList.append(pEnd)
    # show_points_line(paraList)
    geo = sweep_stere(sec, Line(paraList))
    # create_geometry(geo.colorRed())
    return geo



line = [Vec3(0, 0), Vec3(200, -100, 0), Vec3(
    400, 0,100), Vec3(550, 50), Vec3(800, -100, -0)]
# show_points_line(line)  # total
p = Vec3(70, 0,  100)
p = Vec3(-100, 0,  100)
# p = Vec3(0, 70, 100)
# l0 = get_distance_of_point_line(p, Segment(line[0], line[1]))
# l1 = get_distance(line[0], line[1], p)

line = Line(line)
sec = Section(Vec3(), Vec3(50, 0), Vec3(50, 50), Vec3(0, 50))
sec2 = transy(-150)*roty(-pi/2)*Section(Vec3(), Vec3(100, 0), Vec3(100,50, ), Vec3(0, 50,))
sec1 = transy(-100)*roty(-pi/2)*sec
sec0 = transy(-200)*roty(-pi/2)*sec
# _sweep_parallel(sec0, line)
# _sweep_parallel(sec1, line)
# _sweep_parallel(sec2, line)

sec0 = transy(-50)*roty(-pi/2)*sec
sec0=roty(pi/2)*Section(five_points_star(30))
create_geometry(sweep_stere(sec0, line))
exit(0)

is_two_sections_intersect
p1 = dot(Vec3(12, 20), Vec3(10, 20),)*dot(Vec3(20, 12), Vec3(10, 20),)
p2 = Vec3(12, 20) * Vec3(10, 20)*Vec3(20, 12)*Vec3(10, 20)
p3 = (Vec3(12, 20) * Vec3(10, 20))*(Vec3(20, 12)*Vec3(10, 20))


def get_intersect_point_of_two_line(lineA: Segment, lineB: Segment):
    A = lineA.start
    B = lineA.end
    C = lineB.start
    D = lineB.end
    # |(A-C)*(D-C)+k*(B-A)*(D-C)|^2==|(A-C)+k*(B-A)|^2*|(D-C)|^2
    a1 = (B-A)*(D-C)*(B-A)*(D-C)
    b1 = 2*(A-C)*(D-C)*(B-A)*(D-C)
    c1 = (A-C)*(D-C)*(A-C)*(D-C)
    d = (D-C)*(D-C)
    a2 = (B-A)*(B-A)
    b2 = 2*(A-C)*(B-A)
    c2 = (A-C)*(A-C)
    a = a1-d*a2
    b = b1-d*b2
    c = c1-d*c2
    delta = sqrt(b*b-4*a*c)
    # k = -0.5*b/a
    E = A-0.5*b/a*(B-A)

    # 不知道为什么，但是就是很好看
    # grace
    a = (B-A)*(D-C)*(B-A)*(D-C)-(B-A)*(B-A)*(D-C)*(D-C)
    b = (A-C)*(D-C)*(B-A)*(D-C)-(A-C)*(B-A)*(D-C)*(D-C)
    E = A-b/a*(B-A)

    A = lineA.vectorU  # B-A
    B = lineB.vectorU  # D-C
    C = lineA.start - lineB.start  # u=A-C
    a = A*B*A*B-A*A*B*B
    b = C*B*A*B-C*A*B*B
    E = lineA.start-b/a*A

    # corss==0
    # a.y*b.z-a.z*b.y, a.z*b.x-a.x*b.z, a.x*b.y-a.y*b.x
    # a = (A-C)+k*(B-A)
    # b = (D-C)
    # ((A-C).y+k*(B-A).y)*(D-C).z == ((A-C).z+k*(B-A).z)*(D-C).y
    h1 = cross(C-A, B-A)
    h2 = cross(B-A, D-C)
    # h1 = norm(cross(C-A, B-A))
    # h2 = norm(cross(B-A, D-C))
    # E = C+h1.z/h2.z*(D-C)

    return E


ag1 = get_angle_of_two_vectors(Vec3(1, 0), Vec3(1, 1))-pi/4
ag2 = get_angle_of_two_vectors(Vec3(1, 0), Vec3(-1, 1))-pi/4-pi/2

line1 = Segment(Vec3(-38, 0), Vec3(-39, 0))
line2 = Segment(Vec3(0, 38), Vec3(0, 39))
# line1 = Segment(Vec3(0, 0), Vec3(1, 0))
# line2 = Segment(Vec3(2, 0), Vec3(3, 0))
# line1 = Segment(Vec3(0, 0, 0), Vec3(0, 1, 1))
# line2 = Segment(Vec3(0, 2, 0), Vec3(0, 0, 2))

line1 = Segment(Vec3(0, -2), Vec3(1, 0))
line2 = Segment(Vec3(0, 1), Vec3(-2, 0),)

pts = get_intersect_point_of_two_lines(line1, line2, True, True)
pts2 = get_intersect_point_of_two_line(line1, line2)

cone = Cone(Vec3(0, 0, -1), Vec3(0, 0, 1),)
# create_geometry(cone)
# mat = rotx(pi)*roty(-pi/4)*rotz(-pi/2)
# mat = rotz(pi)*roty(-pi/4)*rotx(-pi/2)
# mat = rotx(-pi/2)*roty(-pi/4)*rotz(pi)

# theta c b a 反向拆分角度
mat = rotz(-pi/2)*roty(-pi/3)*rotx(0)
create_geometry(mat*cone)

print()
'''
$(SolutionDir)..\$(Configuration)_sdk\Lib\$(Configuration)\Share\BcgFrame\
$(SolutionDir)..\$(Configuration) sdk\Lib\$(Configuration)\P3DCore\
$(SolutionDir)..\$(Configuration)_sdk\Lib\$(Configuration)\





'''
