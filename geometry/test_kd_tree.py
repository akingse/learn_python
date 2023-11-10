import math
import sys
import os
mypath = r'D:\Alluser\learn_python'  # fixed path
sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
from pyp3d import*

class Node():
    def __init__(self,pt,leftBranch,rightBranch,dimension):
        self.pt = pt
        self.leftBranch = leftBranch
        self.rightBranch = rightBranch
        self.dimension = dimension #depth
 
class KDTree():
    def __init__(self,pts):
        self.nearestPt = None
        self.nearestDis = math.inf
        # using inner cal
        root = self.createKDTree(pts)   
        self.node=root#Node([],None,None,0)

    
    def createKDTree(self,currPts,dimension=0):
        if(len(currPts) == 0):
            return None
        mid = self.calMedium(currPts)
        sortedData = sorted(currPts,key=lambda x:x[dimension])
        leftBranch = self.createKDTree(sortedData[:mid],self.calDimension(dimension))
        rightBranch = self.createKDTree(sortedData[mid+1:],self.calDimension(dimension))
        return Node(sortedData[mid],leftBranch,rightBranch,dimension)

    def calMedium(self,currPts): # 二分计算使用
        return len(currPts) // 2

    def calDimension(self,dimension):# 交替xy方向划分
        return (dimension+1)%2
 
    def calDistance(self,p0,p1): # the norm
        return math.sqrt((p0[0]-p1[0])**2+(p0[1]-p1[1])**2)
 
    #  for search
    def getNearestPt(self,targetPt):
        self.search(self.node, targetPt)
        return self.nearestPt,self.nearestDis
        
    def search(self,node,targetPt):
        # node=self.node
        if node == None: #叶子节点标志
            return
        dist = node.pt[node.dimension] - targetPt[node.dimension]
        if(dist > 0):#目标点在节点的一侧，递归查找，知道叶子节点
            self.search(node.leftBranch,targetPt)
        else:
            self.search(node.rightBranch,targetPt)
        tempDis = self.calDistance(node.pt,targetPt)
        if(tempDis < self.nearestDis):
            self.nearestDis = tempDis
            self.nearestPt = node.pt
        #回溯
        if(self.nearestDis > abs(dist)):
            if(dist > 0):
                self.search(node.rightBranch,targetPt)
            else:
                self.search(node.leftBranch,targetPt)
 
if __name__ == "__main__":

     
    pts = [(5,3),(2.5,5),(8,4.5),(2,2),(3.5,8),(8,2.5),(5.5,7.5)]  #点集
    # create_geometry(Section(Vec3(0,0),Vec3(10,0),Vec3(10,10),Vec3(0,10),))
    # for iter in pts:
    #     create_geometry(Sphere(Vec3(*iter),0.1))

    targetPt = (4.5,7.5)  #目标点
 
    kdtree = KDTree(pts) 
    # root = kdtree.createKDTree(pts)   
    pt,minDis = kdtree.getNearestPt(targetPt)
    print("最近的点是",pt,"最小距离是",str(minDis))