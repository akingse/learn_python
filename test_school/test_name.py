import sys
import os
import re

from sympy import false


mypath = r"D:\Commun\PKPM\Release\PythonScript\python-3.7.9-embed-amd64\Lib\site-packages"
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import *


def get_name_of_obj(obj, except_word=""):
    for name, item in globals().items():
        if item == obj:
            print(name)
            return name


# l = get_list_from_matrix(trans(1, 2, 3))
l = get_list_from_matrix(trans(1, 2, 3), False)
print(l)

objA = [1, 2, 3]
objB = ('a', {'b': 'thi is B'}, 'c')
objC = [{'a1': 'a2'}]
# name = get_name_of_obj(objC)

# for item in [objA, objB, objC]:
#     get_name_of_obj(item)

# for item in [objA, objB, objC]:
#     get_name_of_obj(item, "item")
a = 1

nameAll = globals().items()
lst = list(nameAll)
# print(nameAll)
# for key, value in list(nameAll):
#     # for name, item in nameAll:
#     print(key, value)


b = 2
