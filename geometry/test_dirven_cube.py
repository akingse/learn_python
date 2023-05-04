import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *
from math import *

def setMatrixOfCubeSize(mat: GeTransform, lwh:float, axis:str, isForw=True):
    pos=get_matrixs_position(mat)
    if (axis=='X'):
        axisx = get_matrixs_axisx(mat)
        if(axisx.isOrigin()):
            return mat
        x=lwh/axisx.norm()
        sk=trans(pos)*(trans(-pos)*mat*scale(x,1,1))
        return sk if(isForw) else trans((axisx.norm()-lwh)*axisx.unitize())*sk
    elif (axis=='Y'):
        axisy = get_matrixs_axisy(mat)
        if(axisy.isOrigin()):
            return mat
        y=lwh/axisy.norm()
        sk=trans(pos)*(trans(-pos)*mat*scale(1,y,1))
        return sk if(isForw) else trans((axisy.norm()-lwh)*axisy.unitize())*sk
    elif (axis=='Z'):
        axisz = get_matrixs_axisz(mat)
        if(axisz.isOrigin()):
            return mat
        z=lwh/axisz.norm()
        sk=trans(pos)*(trans(-pos)*mat*scale(1,1,z))
        return sk if(isForw) else trans((axisz.norm()-lwh)*axisz.unitize())*sk
    else:
        return mat
    
# 体心立方体
def getCubeVertexeByIndexCenter(mat: GeTransform, index: int, isAll=False):
    if (not isAll):
        if (index == 0):
            return mat * GeVec3d(-1, -1, -1)
        elif (index == 1):
            return mat * GeVec3d(1, -1, -1)
        elif (index == 1):
            return mat * GeVec3d(1, 1, -1)
        elif (index == 1):
            return mat * GeVec3d(-1, 1, -1)
        elif (index == 1):
            return mat * GeVec3d(-1, -1, 1)
        elif (index == 1):
            return mat * GeVec3d(1, -1, 1)
        elif (index == 1):
            return mat * GeVec3d(1, 1, 1)
        elif (index == 1):
            return mat * GeVec3d(-1, 1, 1)
        else:
            return g_axisNaN
    else:
        return [mat * GeVec3d(-1, -1, -1), mat * GeVec3d(1, -1, -1), mat * GeVec3d(1, 1, -1), mat * GeVec3d(-1, 1, -1),
                mat * GeVec3d(-1, -1, 1), mat * GeVec3d(1, -1, 1), mat * GeVec3d(1, 1, 1), mat * GeVec3d(-1, 1, 1)]


def _origin2center(mat: GeTransform):
    # matS=scale_point(get_matrixs_position(mat),0.5,0.5,0.5)*mat
    # pointC=matS * GeVec3d(0.5,0.5,0.5)
    # return trans(pointC)*get_matrixs_rotation(matS)
    return scale_point(mat * GeVec3d(1, 1, 1), 0.5, 0.5, 0.5)*mat


def _center2origin(mat: GeTransform):
    return scale_point(mat * GeVec3d(1, 1, 1), 2, 2, 2)*mat

# getCubeAllVertexes
def getCubeVertexByIndex(mat: GeTransform, index: int, isAll=False):
    vertexes = []
    # pD0 = getCubeAllVertexes(mat, 0)
    # pD1 = getCubeAllVertexes(mat, 1)
    # pD2 = getCubeAllVertexes(mat, 2)
    # pD3 = getCubeAllVertexes(mat, 3)
    # pD4 = getCubeAllVertexes(mat, 4)
    # pD5 = getCubeAllVertexes(mat, 5)
    # pD6 = getCubeAllVertexes(mat, 6)
    # pD7 = getCubeAllVertexes(mat, 7)
    vertexes.append(mat * GeVec3d(0, 0, 0))
    vertexes.append(mat * GeVec3d(1, 0, 0))
    vertexes.append(mat * GeVec3d(1, 1, 0))
    vertexes.append(mat * GeVec3d(0, 1, 0))
    vertexes.append(mat * GeVec3d(0, 0, 1))
    vertexes.append(mat * GeVec3d(1, 0, 1))
    vertexes.append(mat * GeVec3d(1, 1, 1))
    vertexes.append(mat * GeVec3d(0, 1, 1))
    if isAll:
        return vertexes
    else:
        return vertexes[index]


def _get_circle_center(p1: GeVec2d, p2: GeVec2d, p3: GeVec2d):
    mat = set_matrix_by_row_vectors(
        to_vec3(p2-p1), to_vec3(p3-p1), GeVec3d(0, 0, 1))
    inv = inverse(mat)
    E = inv*mat
    p = inverse(mat) * GeVec3d((p2-p1)*(p2-p1)/2, (p3-p1)*(p3-p1)/2)
    d1 = norm(p-p1)
    d2 = norm(p-p2)
    d3 = norm(p-p3)
    return inverse(mat) * GeVec3d((p2-p1)*(p2-p1)/2, (p3-p1)*(p3-p1)/2)


def _get_theta(p1: GeVec2d, p2: GeVec2d, p3: GeVec2d):
    a = p2-p1
    b = p3-p1
    cos = dot(a, b)/norm(a)/norm(b)
    # res1 = sqrt(1-cos*cos)
    sin = norm(cross(a, b))/norm(a)/norm(b)
    return [cos, sin]


def _cube_get_vertex_from_three_peek_points(p1: GeVec3d, p2: GeVec3d, p3: GeVec3d, isPosi=True):
    # # record every fail way
    # three sphere intersect
    if (is_coincident(p1, p2) or is_coincident(p1, p3) or is_coincident(p3, p2)):
        raise ValueError('')
    mat = get_matrix_from_three_points([p1, p2, p3], False)
    inv = inverse_orth(mat)
    pR1 = inv*p1
    pR2 = inv*p2
    pR3 = inv*p3
    a = pR2-pR1
    b = pR3-pR1
    la = norm(a)
    lb = norm(b)
    cos = dot(a, b)/la/lb
    sin = norm(cross(a, b))/la/lb
    r = 0.5*lb*sin
    cosTheta = (0.25*la*la-(lb*cos-0.5*pR2.x) *
                (lb*cos-0.5*pR2.x)-2*r*r)/(lb*sin*r)
    sinTheta = (2*isPosi-1)*sqrt(1-cosTheta*cosTheta)
    pTheta = GeVec3d(lb*cos, 0.5*lb*sin+r*cosTheta, r *
                     sinTheta)  # the positive solution
    return mat*pTheta

    # mat=set_matrix_by_row_vectors(GeVec3d(Yb*Zc - Yc*Zb, Zb*Xc - Zc*Xb, Xb*Yc - Xc*Yb), GeVec3d(2*Xb,2*Yb,2*Zb), GeVec3d(2*Xc,2*Yc,2*Zc))
    # inv=inverse(mat)
    # return inverse(mat) * GeVec3d(0, Xb*Xb + Yb*Yb + Zb*Zb)

    # mat=set_matrix_by_row_vectors(p2 - p3, p1 - p2, p1 - p3)
    # inv=inverse(mat) #矩阵不可逆，此路不通
    # return inv * GeVec3d(p1 * (p2 - p3), p3 * (p1 - p2), p2 * (p1 - p3))

    # mat = get_matrix_from_three_points([p1, p2, p3], False)
    # inv = inverse(mat)
    # pR1 = inv*p1
    # pR2 = inv*p2
    # pR3 = inv*p3
    # pRc = _get_circle_center(pR1, pR2, pR3)
    # show_points_line([pR1,pR2,pR3,pRc])
    # k = (pRc.x-pR1.x)*(pRc.x-pR2.x)+(pRc.y-pR1.y)*(pRc.y-pR2.y)
    # z = sqrt(-(pRc.x-pR1.x)*(pRc.x-pR2.x)-(pRc.y-pR1.y)*(pRc.y-pR2.y))
    # p=GeVec3d(pRc.x, pRc.y, z)
    # dot2=(p-pR1)*(p-pR2)
    # dot3=(p-pR1)*(p-pR3)
    # dot1=(p-pR2)*(p-pR3)
    # mat=set_matrix_by_row_vectors(2*p2-2*p1,2*p3-2*p1,2*p3-2*p2) # always linear dependent
    # inv = inverse(mat)
    # return inv*GeVec3d(a*a-b*b-norm_2(p1)+norm_2(p2),a*a-c*c-norm_2(p1)+norm_2(p3),b*b-c*c-norm_2(p2)+norm_2(p3))

    # delta1=norm(p2-p1)*norm(p2-p1)
    # delta2=norm(p3-p1)*norm(p3-p1)
    # delta3=norm(p3-p2)*norm(p3-p2)
    # a=sqrt(0.5*(delta1+delta2-delta3))
    # b=sqrt(0.5*(delta1-delta2+delta3))
    # c=sqrt(0.5*(-delta1+delta2+delta3))
    # mat=set_matrix_by_row_vectors(GeVec3d(2*p2.x-2*p1.x,2*p2.y-2*p1.y,2*p2.z-2*p1.z),
    #                               GeVec3d(2*p3.x-2*p1.x,2*p3.y-2*p1.y,2*p3.z-2*p1.z),
    #                               GeVec3d(2*p3.x-2*p2.x,2*p3.y-2*p2.y,2*p3.z-2*p2.z))

    # inv = inverse(mat)
    # return inv*GeVec3d(a*a-b*b-p1.x*p1.x+p2.x*p2.x-p1.y*p1.y+p2.y*p2.y-p1.z*p1.z+p2.z*p2.z,
    #                    a*a-c*c-p1.x*p1.x+p3.x*p3.x-p1.y*p1.y+p3.y*p3.y-p1.z*p1.z+p3.z*p3.z,
    #                    b*b-c*c-p2.x*p2.x+p3.x*p3.x-p2.y*p2.y+p3.y*p3.y-p2.z*p2.z+p3.z*p3.z)


# defualt set change, include multi-solution
def _setCubeDefaultDiagonalBody(mat: GeTransform, pSet: GeVec3d, index: int):
    axisxU = get_matrixs_axisx(mat).unitize()
    axisyU = get_matrixs_axisy(mat).unitize()
    axiszU = get_matrixs_axisz(mat).unitize()
    if (index % 2 == 0):  # odd
        diag = abs(6-index)
    else:
        diag = abs(8-index)
    offset = getCubeVertexByIndex(mat, diag) - pSet
    if (index == 0):
        pOri = pSet
        sk = inverse_orth(set_matrix_by_column_vectors(
            axisxU, axisyU, axiszU)) * offset  # the direction from diag-point
    elif (index == 1):
        sk = inverse_orth(
            set_matrix_by_column_vectors(-axisxU, axisyU, axiszU)) * offset
        pOri = pSet-sk.x*axisxU  # the direction from origin-point
    elif (index == 2):
        sk = inverse_orth(
            set_matrix_by_column_vectors(-axisxU, -axisyU, axiszU)) * offset
        pOri = pSet-sk.x*axisxU-sk.y*axisyU
    elif (index == 3):
        sk = inverse_orth(set_matrix_by_column_vectors(
            axisxU, -axisyU, axiszU)) * offset
        pOri = pSet-sk.y*axisyU
    elif (index == 4):
        sk = inverse_orth(set_matrix_by_column_vectors(
            axisxU, axisyU, -axiszU)) * offset
        pOri = pSet-sk.z*axiszU
    elif (index == 5):
        sk = inverse_orth(
            set_matrix_by_column_vectors(-axisxU, axisyU, -axiszU)) * offset
        pOri = pSet-sk.x*axisxU-sk.z*axiszU
    elif (index == 6):
        sk = inverse_orth(
            set_matrix_by_column_vectors(-axisxU, -axisyU, -axiszU)) * offset
        pOri = pSet-sk.x*axisxU-sk.y*axisyU-sk.z*axiszU
    elif (index == 7):
        sk = inverse_orth(set_matrix_by_column_vectors(
            axisxU, -axisyU, -axiszU)) * offset
        pOri = pSet-sk.y*axisyU-sk.z*axiszU
    matOne = set_matrix_by_column_vectors(
        axisxU, axisyU, axiszU, pOri)*scale(sk)
    return matOne

def _setCubeDefaultAdjacentEdge(mat: GeTransform, pSet: GeVec3d, idLocked: int, indexSet: int, size: str):
    # two points, keep segments on origin plane
    axisxU = get_matrixs_axisx(mat)
    axiszU = get_matrixs_axisz(mat)
    lwh = get_scale_param(mat)
    # effect length (V0 && V1, V2 && V3, V4 && V5, V6 && V7)
    if (size == 'length'):
        axisX = pSet-getCubeVertexByIndex(mat, idLocked)
        axisY = unitize(axiszU ^ axisX)
        axisZ = unitize(axisX ^ axisY)
        pOri = getCubeVertexByIndex(mat, idLocked)
        if idLocked == 0 and indexSet == 1:
            pass
        elif idLocked == 1 and indexSet == 0:
            axisX = -axisX  # opposite-dirction
            axisY = -axisY  # 2 negatives make a positive
            pOri = pSet
        elif idLocked == 3 and indexSet == 2:
            pOri = pOri-lwh.y*axisY
        elif idLocked == 2 and indexSet == 3:
            axisX = -axisX
            axisY = -axisY
            pOri = pSet-lwh.y*axisY
        elif idLocked == 4 and indexSet == 5:
            pOri = pOri-lwh.z*axisZ
        elif idLocked == 5 and indexSet == 4:
            axisX = -axisX
            axisY = -axisY
            pOri = pSet-lwh.z*axisZ
        elif idLocked == 7 and indexSet == 6:
            pOri = pOri-lwh.z*axisZ-lwh.y*axisY
        elif idLocked == 6 and indexSet == 7:
            axisX = -axisX
            axisY = -axisY
            pOri = pSet-lwh.z*axisZ-lwh.y*axisY
        # merge
        mat = set_matrix_by_column_vectors(
        axisX, lwh.y*axisY, lwh.z*axisZ, pOri)
    # effect width  (V0 && V3, V1 && V2, V4 && V7, V5 && V6)
    elif (size == 'width'):
        axisY = pSet-getCubeVertexByIndex(mat, idLocked)
        axisX = unitize(axisY ^ axiszU)
        axisZ = unitize(axisX ^ axisY)
        pOri = getCubeVertexByIndex(mat, idLocked)
        if idLocked == 0 and indexSet == 3:
            pass
        elif idLocked == 1 and indexSet == 0:
            axisY = -axisY
            axisX = -axisX 
            pOri = pSet
        elif idLocked == 1 and indexSet == 2:
            pOri = pOri-lwh.x*axisX
        elif idLocked == 2 and indexSet == 1:
            axisY = -axisY
            axisX = -axisX 
            pOri = pSet-lwh.x*axisX
        elif idLocked == 4 and indexSet == 7:
            pOri = pOri-lwh.z*axisZ
        elif idLocked == 7 and indexSet == 4:
            axisY = -axisY
            axisX = -axisX 
            pOri = pSet-lwh.z*axisZ
        elif idLocked == 5 and indexSet == 6:
            pOri = pOri-lwh.x*axisX-lwh.z*axisZ
        elif idLocked == 6 and indexSet == 5:
            axisY = -axisY
            axisX = -axisX 
            pOri = pSet-lwh.x*axisX-lwh.z*axisZ
        mat = set_matrix_by_column_vectors(
        lwh.x*axisX, axisY, lwh.z*axisZ, pOri)
    # effect height (V0 && V4, V1 && V5, V2 && V6, V3 && V7)
    elif (size == 'height'):
        axisZ = pSet-getCubeVertexByIndex(mat, idLocked)
        axisY = unitize(axisZ ^ axisxU)
        axisX = unitize(axisY ^ axisZ)
        pOri = getCubeVertexByIndex(mat, idLocked)
        if idLocked == 0 and indexSet == 4:
            pass
        elif idLocked == 4 and indexSet == 0:
            axisZ = -axisZ
            axisY = -axisY
            pOri = pSet
        elif idLocked == 1 and indexSet == 5:
            pOri = pOri-lwh.x*axisX
        elif idLocked == 5 and indexSet == 1:
            axisZ = -axisZ
            axisY = -axisY
            pOri = pSet-lwh.x*axisX
        elif idLocked == 3 and indexSet == 7:
            pOri = pOri-lwh.y*axisY
        elif idLocked == 7 and indexSet == 3:
            axisZ = -axisZ
            axisY = -axisY
            pOri = pSet-lwh.y*axisY
        elif idLocked == 2 and indexSet == 6:
            pOri = pOri-lwh.x*axisX-lwh.y*axisY
        elif idLocked == 6 and indexSet == 2:
            axisZ = -axisZ
            axisY = -axisY
            pOri = pSet-lwh.x*axisX-lwh.y*axisY
        mat = set_matrix_by_column_vectors(
        lwh.x*axisX, lwh.y*axisY, axisZ, pOri)
    return mat

# Python to C++:
def _setCubeDefaultDiagonalFace(mat: GeTransform, pSet: GeVec3d, idLocked: int, indexSet: int, type: str):
    axisxU = get_matrixs_axisx(mat).unitize()
    axisyU = get_matrixs_axisy(mat).unitize()
    lwh = get_scale_param(mat)
    pOri = getCubeVertexByIndex(mat, idLocked)
    vecDia = pSet-pOri
    if (type=='XOY'):
        # one kind of strategy
        axisZ = unitize(axisxU ^ vecDia)
        axisY = unitize(axisZ ^ axisxU)
        dL = dot(vecDia, axisxU) #/norm(axisxU) # dL=d*cosO
        dW = dot(vecDia, axisY) #/norm(axisY)
        # rotate around local x
        if idLocked == 0 and indexSet == 2:
            pass
        elif idLocked == 2 and indexSet == 0:
            # vecDia=-vecDia
            axisZ = -axisZ
            axisY = -axisY
            dL = -dL
            pOri=pSet
        elif idLocked == 4 and indexSet == 6: #parallel
            pOri=pOri-lwh.z*axisZ
        elif idLocked == 6 and indexSet == 4:
            axisZ = -axisZ
            axisY = -axisY
            dL = -dL
            pOri=pSet-lwh.z*axisZ
        # cross line
        elif idLocked == 1 and indexSet == 3:
            dL = -dL #obtuse angle
            pOri=pOri-dL*axisxU
        elif idLocked == 3 and indexSet == 1:
            axisZ = -axisZ
            axisY = -axisY #--=+
            pOri=pSet-dL*axisxU
        elif idLocked == 5 and indexSet == 7:
            dL = -dL #obtuse angle
            pOri=pOri-dL*axisxU-lwh.z*axisZ
        elif idLocked == 7 and indexSet == 5:
            axisZ = -axisZ
            axisY = -axisY #--=+
            pOri=pSet-dL*axisxU-lwh.z*axisZ
        mat = set_matrix_by_column_vectors(
            dL*axisxU, dW*axisY, lwh.z*axisZ, pOri)
    elif (type=='XOZ'):
        axisY = unitize(vecDia ^ axisxU)
        axisZ = unitize(axisxU ^ axisY)
        dL = dot(vecDia, axisxU) #/norm(axisxU) # dL=d*cosO
        dH = dot(vecDia, axisZ) #/norm(axisY)
        if idLocked == 0 and indexSet == 5:
            pass
        elif idLocked == 5 and indexSet == 0:
            axisZ = -axisZ
            axisY = -axisY
            dL = -dL
            pOri=pSet
        elif idLocked == 3 and indexSet == 6:
            pOri=pOri-lwh.z*axisZ
        elif idLocked == 6 and indexSet == 3:
            axisZ = -axisZ
            axisY = -axisY
            dL = -dL
            pOri=pSet-lwh.z*axisZ
        # cross line
        elif idLocked == 1 and indexSet == 4:
            dL = -dL
            pOri=pOri-dL*axisxU
        elif idLocked == 4 and indexSet == 1:
            axisZ = -axisZ
            axisY = -axisY
            dL = -dL
            pOri=pSet-dL*axisxU
        elif idLocked == 2 and indexSet == 7:
            dL = -dL
            pOri=pOri-dL*axisxU-lwh.z*axisZ
        elif idLocked == 7 and indexSet == 2:
            axisZ = -axisZ
            axisY = -axisY
            dL = -dL
            pOri=pSet-dL*axisxU-lwh.z*axisZ
        mat = set_matrix_by_column_vectors(
            dL*axisxU, lwh.y*axisY, dH*axisZ, pOri)
    elif (type=='YOZ'):
        axisX = unitize(axisyU ^ vecDia)
        axisZ = unitize(axisX ^ axisyU)
        dW = dot(vecDia, axisyU) #/norm(axisxU) # dL=d*cosO
        dH = dot(vecDia, axisZ) #/norm(axisY)
        if idLocked == 0 and indexSet == 7:
            pass
        elif idLocked == 7 and indexSet == 0:
            axisX = -axisX
            axisZ = -axisZ
            dW = -dW
            pOri=pSet
        elif idLocked == 1 and indexSet == 6:
            pOri=pOri-lwh.x*axisX
        elif idLocked == 6 and indexSet == 1:
            axisX = -axisX
            axisZ = -axisZ
            dW = -dW
            pOri=pSet-lwh.x*axisX
        # cross line
        elif idLocked == 3 and indexSet == 4:
            dW = -dW
            pOri=pOri-dW*axisyU
        elif idLocked == 4 and indexSet == 3:
            axisX = -axisX
            axisZ = -axisZ
            pOri=pSet-dW*axisyU
        elif idLocked == 2 and indexSet == 5:
            dW = -dW
            pOri=pOri-dW*axisyU-lwh.x*axisX
        elif idLocked == 5 and indexSet == 2:
            axisX = -axisX
            axisZ = -axisZ
            pOri=pSet-dW*axisyU-lwh.x*axisX
        mat = set_matrix_by_column_vectors(
            lwh.x*axisX, dW*axisyU, dH*axisZ, pOri)
    return mat




# -------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------------------
# trans(100,0)*rotx(pi/6)*roty(pi/6)*
cube = rotz(pi/6)*trans(100, 0)*scale(300, 200, 100)*Cube()
create_geometry(cube)
show_points_line(getCubeVertexByIndex(cube.transformation, 0, True))
# create_geometry(trans(getCubeAllVertexes(cube.transformation,0))*scale(10)*Sphere())

# 面对角线
idLocked=0
idSet=7
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(400, 200, 100), 0, 2, 'XOY')
mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(0, 300, 300), 1, 3, 'XOY')
mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(300, 300, 300), 3, 1, 'XOY')
mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(0, 300, 300), 5, 7, 'XOY')
mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(300, 300, 300),7,  5, 'XOY')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(300, 0, 300), idLocked, idSet, 'XOZ')

# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(100, 300, 300), 0, 7, 'YOZ')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(300, 0, 0), 7, 0, 'YOZ')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(0, 0, 300), 3, 4, 'YOZ')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(300, 300, 0), 4, 3, 'YOZ')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(500, 500, 200), 1, 6, 'YOZ')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(500, 0, 0), 6, 1, 'YOZ')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(500, 500, 0), 5, 2, 'YOZ')
# mat=_setCubeDefaultDiagonalFace(cube.transformation, Vec3(500, 0, 500), 2, 5, 'YOZ')
# create_geometry(mat*Cube())
# print(getCubeAllVertexes(mat,7))
# vertify
# print(get_scale_param(mat))
# sk=get_scale_param(mat)
# print(norm_2(getCubeAllVertexes(mat,7)-getCubeAllVertexes(mat,0))-(sk.y**2+sk.z**2))
# show_points_line(getCubeAllVertexes(mat, 0, True))
# show_points_line([pSet,getCubeAllVertexes(mat, idLocked)])


# mat=setMatrixOfCubeSize(cube.transformation,400,'Z',True)
# mat=setMatrixOfCubeSize(cube.transformation,400,'Z',False)
# mat=setMatrixOfCubeSize(cube.transformation,400,'X',True)
# mat=setMatrixOfCubeSize(cube.transformation,400,'X',False)
# create_geometry(mat*Cube())


# 测试两点参数驱动
# _setCubeDefault2(mat: GeTransform, pSet: GeVec3d, idLocked: int, indexSet: int)
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 300, 0), 2, 3)
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(500, 0, 0), 4, 5,'length')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, -100, 0), 5, 4,'length')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(-500, 100, 0), 7, 6,'length')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, -100, 0), 6, 7,'length')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 500, -100), 0, 3,'width')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 500, 0), 4, 7,'width')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 0, -100), 7, 4,'width')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 500, 200), 5, 6,'width')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 500, -100), 6, 5,'width')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 100, 300), 0, 4,'height')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 100, 300), 3, 7,'height')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 100, 300), 2, 6,'height')
# mat = _setCubeDefaultAdjacentEdge(cube.transformation, Vec3(0, 100, 300), 6, 2,'height')

# create_geometry(mat*Cube())
# show_points_line(getCubeAllVertexes(mat, 0, True))


# ---------------------------------------------------------------------------------------------


V0 = getCubeVertexByIndex(cube.transformation, 0)
V1 = getCubeVertexByIndex(cube.transformation, 1)
V2 = getCubeVertexByIndex(cube.transformation, 2)
V3 = getCubeVertexByIndex(cube.transformation, 3)
V4 = getCubeVertexByIndex(cube.transformation, 4)
V5 = getCubeVertexByIndex(cube.transformation, 5)
V6 = getCubeVertexByIndex(cube.transformation, 6)
V7 = getCubeVertexByIndex(cube.transformation, 7)
# sphere1 = trans(0.5*(p0+p2))*scale(0.5*norm(p0-p2))*Sphere()
# sphere2 = trans(0.5*(p0+p5))*scale(0.5*norm(p0-p5))*Sphere()
# sphere3 = trans(0.5*(p5+p2))*scale(0.5*norm(p5-p2))*Sphere()
# create_geometry(trans(p0)*scale(10)*Sphere())
# create_geometry(trans(p2)*scale(10)*Sphere())
# create_geometry(trans(p5)*scale(10)*Sphere())
# create_geometry(Section(p0, p2, p5).colorRed())
# create_geometry(Line(p1, p7))
# create_geometry(Section(p3, p4, p6))
# create_geometry(sphere1)
# create_geometry(sphere2)
# create_geometry(sphere3)

# bl = is_perpendi(p1-p7, cross(p2-p0, p5-p2))
# # dp=get_distance_of_point_plane(p1,get_matrix_from_three_points([p0,p2,p5]))
# mat = get_matrix_from_three_points([p0, p2, p5])
# dp = get_intersect_point_of_line_plane(
#     Segment(p1, p7), get_matrix_from_three_points([p0, p2, p5]))[0]
# create_geometry(trans(dp)*scale(10)*Sphere())
# d3=norm(p1-dp)

# 测试三点求解立方体
point = _cube_get_vertex_from_three_peek_points(V0, V2, V5)
point = _cube_get_vertex_from_three_peek_points(V0, V2, V7,False)
point = _cube_get_vertex_from_three_peek_points(V1, V3, V4,False)
point = _cube_get_vertex_from_three_peek_points(V1, V3, V6)

point = _cube_get_vertex_from_three_peek_points(V4, V6, V1,False)
point = _cube_get_vertex_from_three_peek_points(V4, V6, V3)
point = _cube_get_vertex_from_three_peek_points(V5, V7, V0)
point = _cube_get_vertex_from_three_peek_points(V5, V7, V2,False)

create_geometry(trans(point)*scale(10)*Sphere().colorBlue())
# show_points_line([p0,p0+1/3*(p2-p0+p5-p0)])
# show_points_line([p0,p0+100*cross(p2-p0,p5-p0).unitize()])

# 测试单点参数驱动
# mat=_setCubeDefault(cube.transformation,Vec3(500,400,200),7)
# create_geometry(mat*Cube())
# show_points_line(getCubeAllVertexes(mat,0,True))


# cubeC=_origin2center(cube.transformation)
# show_points_line(getCubeVertexeByIndexCenter(cubeC,-1,True))
# create_geometry(cubeC*Cube())
# show_coordinate_system(get_orthogonal_matrix(cubeC))
# create_geometry(_center2origin(cubeC)*Cube()) #反向

# 三角形外接圆心
# create_geometry(Section(p0,p1,p2))
# point=_get_circle_center(p0,p1,p2)
# create_geometry(trans(point)*scale(10)*Sphere())


'''
位置 xyz
欧拉角 rpy
镜像轴 x y z /镜像平面 xoy xoz yoz
缩放系数 kx ky kz
'''

# mat=rotz(pi/2)*roty(pi/3)*rotz(pi/4)
# print_matrix(mat)
# rpy=get_rot_matrix_angle(mat)
# print(degrees(rpy[0]),degrees(rpy[1]),degrees(rpy[2]))

# 世界坐标系下的xyz欧拉角
# 旋转角度(α,β,γ),旋转顺序(x->y->z),内旋.

matR=rotx(pi/2)*roty(pi/3)*rotz(pi/4)
res=get_rot_matrix_angle_euler(matR)
# print(degrees(res[0]),degrees(res[1]),degrees(res[2]))

mat1=g_matrixO
mat2=trans(1,2)*mat1
p1=mat2*Vec3(2,1)
p2=trans(1,2)*Vec3(2,1)

import sympy
import symbol
from sympy import *
t1=sympy.Symbol('t1')
t2=sympy.Symbol('t2')
t3=sympy.Symbol('t3')
# x, y, z, t = symbol('x,y,z,t')
t1 = symbols('x')
t2 = symbols('y')
t3 = symbols('z')
# print(sin(t1)+cos(t2))
exit()
# mat=rotz(t1)*roty(t2)*rotx(t3)
# [ cos(t1)*cos(t2), cos(t1)*sin(t2)*sin(t3) - cos(t3)*sin(t1), sin(t1)*sin(t3) + cos(t1)*cos(t3)*sin(t2)]
# [ cos(t2)*sin(t1), cos(t1)*cos(t3) + sin(t1)*sin(t2)*sin(t3), cos(t3)*sin(t1)*sin(t2) - cos(t1)*sin(t3)]
# [        -sin(t2),                           cos(t2)*sin(t3),                           cos(t2)*cos(t3)]



# using this method
# mat=rotx(t1)*roty(t2)*rotz(t3)
# [                           cos(t2)*cos(t3),                          -cos(t2)*sin(t3),          sin(t2)]
# [ cos(t1)*sin(t3) + cos(t3)*sin(t1)*sin(t2), cos(t1)*cos(t3) - sin(t1)*sin(t2)*sin(t3), -cos(t2)*sin(t1)]
# [ sin(t1)*sin(t3) - cos(t1)*cos(t3)*sin(t2), cos(t3)*sin(t1) + cos(t1)*sin(t2)*sin(t3),  cos(t1)*cos(t2)]
