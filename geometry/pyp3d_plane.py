import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..//'))
from pyp3d import *


class Plane():  # 几何概念-平面
    # 几种默认构造
    # 1 三点式（两个向量）
    # 2 一般式 # Ax+By+Cz+D=0
    # 3 平面法向量（点法式）
    # 4 矩阵形式（默认XoY面）
    def __init__(self, *args):
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        if len(args) == 1 and isinstance(args[0], GeTransform):
            mat = get_orthogonal_matrix(args[0])
            vecZ = get_matrixs_axisz(mat)
            point = get_matrixs_position(mat)
            self.A = vecZ.x
            self.B = vecZ.y
            self.C = vecZ.z
            self.D = -(self.A*point.x+self.B*point.y+self.C*point.z)
        # elif len(args) == 3 and is_all_vec(args):
        #     self.m_mat = get_matrix_from_three_points(args)
        elif len(args) == 4 and is_all_num(args):
            # Ax+By+Cz+D=0
            self.A = args[0]
            self.B = args[1]
            self.C = args[2]
            self.D = args[3]
            if is_float_zero(self.A) and is_float_zero(self.B) and is_float_zero(self.C):
                raise ValueError('parameter error, A&B&C!=0!')
        else:
            raise ValueError('parameter error!')

    def get_matrix(self):
        if is_float_zero(self.A) and is_float_zero(self.B) and is_float_zero(self.C):
            return g_matrixO
        vecZ = GeVec3d(self.A, self.B, self.C)
        if not is_float_zero(self.C):
            point = GeVec3d(0, 0, -self.D/self.C)
        elif not is_float_zero(self.B):
            point = GeVec3d(0, -self.D/self.B, 0)
        else:
            point = GeVec3d(-self.D/self.A, 0, 0)
        mat = get_matrix_from_two_points(point, point+vecZ, True)
        return mat


