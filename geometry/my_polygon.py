# 判断点是否在多边形内部
# https://blog.csdn.net/lynon/article/details/82015834

# if (p.x < minX || p.x > maxX || p.y < minY || p.y > maxY) 
#      return False


# 接下来是核心算法部分：
 
'''int pnpoly (int nvert, float *vertx, float *verty, float testx, float testy) {
    int i, j, c = 0;
    for (i = 0, j = nvert-1; i < nvert; j = i++) {
        if ( ( (verty[i]>testy) != (verty[j]>testy) ) &&
(testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
            c = !c;
    }
    return c;
}
'''

# --------------------------------------------------------
# Topological Polygon Self Intersection Judgment
# 判断点集组成的多边形的方向 
# 判断多边形是否自相交

# 中间问题
# 1 图形面积
# 2 判断点是否在图形内部
# 3 判断两个线段是否相交






# -------------------------------------
# 一个简单的方法，
# 判断任意两条直线是否相交；
# 1 两点直线方程，
# 2 点在直线两侧的判断
A=[0,0]
B=[1,0]
C=[1,1]
D=[0,1]
pointList=[A,B,C,D]

print([i for i in pointList])

print(max(1,2))

# 直线的一般式方程 Ax+By+C=0 （A，B不全为零）
# 一般式:Ax+By+C=0(A、B不同时为0)【适用于所有直线】

# 两点式
# (y-y1)*(y2-y1)+(x-x1)*(x2-x1)=0

# ------------------------------------------------------------
# https://www.jianshu.com/p/ba03c600a557
# 线法的关键是正确计算射线与每条边是否相交。并且规定线段与射线重叠或者射线经过线段下端点属于不相交。
# 首先排除掉不相交的情况
def isRayIntersectsSegment(poi,s_poi,e_poi): #[x,y] [lng,lat]
    #输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    if s_poi[1]==e_poi[1]: #排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]: #线段在射线上边
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]: #线段在射线下边
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]: #交点为下端点，对应spoint
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]: #交点为下端点，对应epoint
        return False
    if s_poi[0]<poi[0] and e_poi[1]<poi[1]: #线段在射线左边
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1]) #求交
    if xseg<poi[0]: #交点在射线起点的左侧
        return False
    return True  #排除上述情况之后


def isPoiWithinPoly(poi,poly):
    #输入：点，多边形三维数组
    #poly=[[[x1,y1],[x2,y2],……,[xn,yn],[x1,y1]],[[w1,t1],……[wk,tk]]] 三维数组

    #可以先判断点是否在外包矩形内 
    #if not isPoiWithinBox(poi,mbr=[[0,0],[180,90]]): return False
    #但算最小外包矩形本身需要循环边，会造成开销，本处略去
    sinsc=0 #交点个数
    for epoly in poly: #循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
        for i in range(len(epoly)-1): #[0,len-1]
            s_poi=epoly[i]
            e_poi=epoly[i+1]
            if isRayIntersectsSegment(poi,s_poi,e_poi):
                sinsc+=1 #有交点就加1

    return True if sinsc%2==1 else  False




# i=0
# if i==1:
#     pass
# P=[]
# NodeVector = linspace(0, 1, n+k+2); % 均匀B样条的节点矢量
# # % 绘制样条曲线
# line(P(1, 1:n+1), P(2, 1:n+1));
# Nik = zeros(n+1, 1);
# for u = k/(n+k+1) : 0.001 : (n+1)/(n+k+1)
#     for i = 0 : 1 : n
#         Nik(i+1, 1) = BaseFunction(i, k , u, NodeVector);
# p_u = P * Nik;
# line(p_u(1,1), p_u(2,1), 'Marker','.','LineStyle','-', 'Color',[.3 .6 .9]);


def B_spline(p_list):
	"""
	:param p_list: (list of list of int:[[x0, y0], [x1, y1], ...])point set of p
	result: (list of list of int:[[x0, y0], [x1, y1], ...])point on curve
	绘制三次(四阶)均匀B样条曲线
	"""
	result = []
	n = len(p_list)
	k = 4
	u = k-1
	while (u < n+1):
		x, y = 0, 0
		#calc P(u)
		for i in range(0, n):
			B_ik = deBoor_Cox(u, k, i)
			x += B_ik * p_list[i][0]
			y += B_ik * p_list[i][1]
		# result.append((int(x+0.5), int(y+0.5)))
		result.append((x, y))
		u += 1/100 #2020/09/27
	return result

def deBoor_Cox(u, k, i):
	if k==0:
		if i <= u and u <= i+1:
			return 1
		else:
			return 0
	else:
		coef_1, coef_2 = 0, 0
		if (u-i == 0) and (i+k-i == 0):
			coef_1 = 0
		else:
			coef_1 = (u-i) / (i+k-i)
		if (i+k+1-u == 0) and (i+k-i == 0):
			coef_2 = 0
		else:
			coef_2 = (i+k+1-u) / (i+k-i)
	return coef_1 * deBoor_Cox(u, k-1, i) + coef_2 * deBoor_Cox(u, k-1, i+1)

p_list=[[0,0],[100,100],[200,0]]
r=B_spline(p_list)
for i in r:
    print(i)
