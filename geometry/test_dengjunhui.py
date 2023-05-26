import sys
import os
import functools
sys.path.append(os.path.join(os.path.dirname(__file__), "..//"))
from pyp3d import *


# ToLeft 单边测试
trig = []


def test_ToLeft(p: GeVec2d, q: GeVec2d, s: GeVec2d) -> bool:
    a = q-p
    b = s-p
    # cros = a.x*b.y-a.y*b.x  # using vecter cross product
    # return cros  # cross(q-p, s-p)
    # using determinant value
    Area2 = p.x*q.y-p.y*q.x +\
        q.x*s.y-q.y*s.x +\
        s.x*p.y-s.y*p.x
    # return Area2
    return Area2 >= 0 # on the line isnot toleft
# 外网暂不支持矢量operator * ^


def merge(arry: list, left: int, middle: int, right: int):  # 归并排序
    temp = (right - left + 1)*[0]
    for i in range(left, right+1):
        temp[i - left] = arry[i]  # copy to temp-array
    i = left
    j = middle + 1
    for k in range(left, right+1):
        if (i > middle and j <= right):
            arry[k] = temp[j - left]
            j += 1
        elif (j > right and i <= middle):
            arry[k] = temp[i - left]
            i += 1
        elif (temp[i - left] > temp[j - left]):  # comparer
            #
            arry[k] = temp[j - left]
            j += 1
        elif (temp[i - left] <= temp[j - left]):  # comparer
            #
            arry[k] = temp[i - left]
            i += 1


def test_MergeSort(arry: list, left: int, right: int):
    if (left >= right):
        return
    middle = int((right + left) / 2)
    test_MergeSort(arry, left, middle)
    test_MergeSort(arry, middle + 1, right)
    merge(arry, left, middle, right)


def merge_vector(arry: list, left: int, middle: int, right: int, ltl: GeVec3d):  # 归并排序
    temp = (right - left + 1)*[0]
    for i in range(left, right+1):
        temp[i - left] = arry[i]  # copy to temp-array
    i = left
    j = middle + 1
    for k in range(left, right+1):
        if (i > middle and j <= right):
            arry[k] = temp[j - left]
            j += 1
        elif (j > right and i <= middle):
            arry[k] = temp[i - left]
            i += 1
        # (temp[i - left] > temp[j - left]):  # comparer
        elif (not test_ToLeft(ltl, temp[i - left], temp[j - left])):
            #
            arry[k] = temp[j - left]
            j += 1
        elif (test_ToLeft(ltl, temp[i - left], temp[j - left])):  # comparer
            #
            arry[k] = temp[i - left]
            i += 1


# 排序预处理
def test_MergeSort_vector(arry: list, left: int, right: int):
    if (left >= right):
        return
    middle = int((right + left) / 2)
    ltl = arry[test_LTL(arry)]
    test_MergeSort_vector(arry, left, middle)
    test_MergeSort_vector(arry, middle + 1, right)
    merge_vector(arry, left, middle, right, ltl)


def test_InTriangle(p: GeVec2d, triangle: list) -> bool:
    b1 = test_ToLeft(p, triangle[0], triangle[1])  # both ccw and cw
    b2 = test_ToLeft(p, triangle[1], triangle[2])
    b3 = test_ToLeft(p, triangle[2], triangle[0])
    return (b1 and b2 and b3) or not ((b1 and b2 and b3))


def test_LTL(S: list):
    # lowest then leftmost
    ltl = 0
    for i in range(len(S)):
        if(S[i].y < S[ltl].y or (S[i].y == S[ltl].y and S[i].x < S[ltl].x)):
            ltl = i
    return ltl


ltl = Vec3()


def compare_toleft(x, y):
    global ltl
    bl = test_ToLeft(ltl, x, y)
    return 1 if (test_ToLeft(ltl, x, y)) else -1


def compare_points(points: list):
    global ltl
    ltl = points[test_LTL(points)]
    # newList = copy.deepcopy(points)
    points.sort(key=functools.cmp_to_key(compare_toleft), reverse=True)
    # return newList


def test_GrahamScan(points: list):
    # 1 Preprocessing sort预排序，使用一种排序（归并排序），自定义比较器
    # 2 处理 back track
    compare_points(points)
    stackS = [points[0], points[1]]
    stackT = []
    n = len(points)
    for i in range(n-3):
        stackT.append(points[n-1-i])
    while(len(stackT) != 0):
        if test_ToLeft(stackS[-2], stackS[-1], stackT[-1]):
            # U, V为栈S的次栈顶和栈顶，W为T的栈顶
            stackS.append(stackT.pop())  # W pop出来 push至S栈中
        else:
            stackS.pop()
    return stackS
    # 推证正确性
    # 欧拉公式： planar graphic with vertexes has O(3n) edges


def my_compare(x, y):
    # if x == y:
    #     return 0
    return 1 if (x > y) else -1
    # if x > y:
    #     return 1
    # elif x < y:
    #     return -1
    # return 0


A = [1, 2, 4, 3, 5, 3, 9, 7]
B = [11, 12, 14, 13, 15]
A.append(B.pop())
# test_MergeSort(A, 0, len(A)-1)
# print(A)
# A.sort(key=functools.cmp_to_key(my_compare))
# print(A)

line = [Vec3(),  Vec3(0, 200), Vec3(200, 100), ]
line = [Vec3(), Vec3(200, 100),  Vec3(0, 200), ]
line = [Vec3(-100, -100), Vec3(200, 0), Vec3(250, 100), Vec3(),
        Vec3(200, 200), Vec3(100, -50), Vec3(120, 100), Vec3(100, 200), Vec3(-100, 300)]
# show_points_line(line)
p = Vec3(100, 0)
p = Vec3(100, 100)
p = Vec3(100, 50)
# show_points_line([p])
# test_MergeSort_vector(line, 0, len(line)-1)
# compare_points(line)

line = test_GrahamScan(line)
# line = compare_points(line)
show_points_line(line)


a = test_ToLeft(line[0], line[1], p)
t = test_InTriangle(p, line)
print(a)
