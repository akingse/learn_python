from .pyp3d_api import *
import os
import sys

class Tool:
    def __init__(self):
      launch_tool(sys.argv[0])
    def getKeyEvent(self):...#读取C++那边的存下来的变量
    def getentityID(self):...
    def getCurrentPoint(self):...
    def getCachePoint(self):
        print("ddddddddddddddddddddddddddddddddddd")
    def settransform(trans):...# 设置动态显示矩阵，剩下的graphic,由 pyhton传过去C++生成

Tool = Tool()
 