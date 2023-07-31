from math import *
import sys
import os
path_p3d = r'D:/Alluser/learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), path_p3d))
path_fbs = r'C:\Users\Aking\source\repos\bimbase\Include'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), path_fbs))
from pyp3d import *  # NOQA: E402
import flatbuffers
from fbs import *  # NOQA: E402

# 从 FlatBuffer 文件中加载二进制数据
filename=r'C:\Users\Aking\source\repos\bimbase\src\P3d2Stl\bin_file\cvtMeshVct_cube2.bin'
with open(filename, 'rb') as file:
    buffer = file.read()

# 反序列化 FlatBuffer 数据
cvtMesh = ConvertToMesh.GetRootAsConvertToMesh(buffer, 0)
box=cvtMesh.AabbMin()
vob=cvtMesh.Vbo().VbosLength()
iob=cvtMesh.Ibo().IbosLength()
triList = MeshVct.GetRootAsMeshVct(buffer, 0)

for i in range(cvtMesh.IboRawLength()):
    triangle = cvtMesh.Ibo(i)

print()