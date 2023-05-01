from sympy import *
import sympy as sy
x,y = sy.symbols("x y")
c,s = sy.symbols("c s")
ax,ay,bx,by = sy.symbols("ax ay bx by")


# zyz=trotz(th4)*troty(th5)*trotz(th6);
# % answer=
# % [-sin(th4)*sin(th6) + cos(th4)*cos(th5)*cos(th6), - sin(th4)*cos(th6) - cos(th4)*cos(th5)*sin(th6), cos(th4)*sin(th5), 0]
# % [ cos(th4)*sin(th6) + sin(th4)*cos(th5)*cos(th6),   cos(th4)*cos(th6) - sin(th4)*cos(th5)*sin(th6), sin(th4)*sin(th5), 0]
# % [                             -sin(th5)*cos(th6),                                sin(th5)*sin(th6),          cos(th5), 0]
# % [                                              0,                                                0,                 0, 1]

import numpy as np
from math import *
two_dim_matrix_one = np.array([[1, 2, 3], [4, 5, 6], [0, 0, 0]])
two_dim_matrix_two = np.array([[1, 2, 3], [4, 5, 6], [0, 0, 0]])
two_multi_res = np.dot(two_dim_matrix_one, two_dim_matrix_two)

T1=np.array([[ax, bx, 0], [ay, by, 0], [0, 0, 0]])
# T2=np.array([[cos(the), -sin(the), 0], [sin(the), cos(the), 0], [0, 0, 1]])
T2=np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
T=np.dot(T1,T2)
# print(T)

c1,s1,c2,s2,c3,s3=sy.symbols("c1 s1 c2 s2 c3 s3")
Z1=np.array([[c1, -s1, 0], [s1, c1, 0], [0, 0, 1]])
Y2=np.array([[c2, 0, s2], [0, 1, 0], [-s2, 0, c2]])
Z3=np.array([[c3, -s3, 0], [s3, c3, 0], [0, 0, 1]])

T=np.multiply(Z1,Y2)
T=np.multiply(T,Z3)

print(T)

# node=[[0],[0]]
# print(node)
# node[0][0]=1
# print(node)