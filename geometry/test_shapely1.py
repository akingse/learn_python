import matplotlib.pyplot as plt
from shapely.ops import unary_union
from shapely.geometry import MultiPolygon
from shapely.geometry import MultiLineString
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon
from shapely.geometry.polygon import LinearRing
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely import *
import numpy as np
import sys
import os
# mypath = 'D:\Alluser\learn_python'  # include pyp3d
# sys.path.append(os.path.join(os.path.dirname(__file__), mypath))
# from pyp3d import *  # NOQA: E402



import matplotlib.pyplot as plt # matplotlib 数据可视化
import geopandas as gpd

poly_union = gpd.GeoSeries([Polygon([(0,0), (0,2), (1,2), (1,3),
(2,3), (2,4), (3, 4), (3, 5), (5, 5), (5, 3), (4, 3), (4, 2),
(3,2), (3,1), (2, 1), (2, 0), (0, 0)])])

# poly_union.plot(color = 'blue')
# plt.show()

