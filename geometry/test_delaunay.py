import numpy as np
import pylab as pl
from scipy import spatial
# points2d = np.array([[0.2, 0.1], [0.5, 0.5], [0.8, 0.1],[0.5, 0.8], [0.3, 0.6], [0.7, 0.6], [0.5, 0.351]])
# vo = spatial.Voronoi(points2d)
x = np.array([46.445, 263.251,174.176, 280.899, 280.899, 189.358, 135.521, 29.638, 101.907, 226.665])
y = np.array([287.865, 250.891, 287.865, 160.975, 54.252, 160.975, 232.404, 179.187, 35.765, 71.361])
points2d = np.c_[x, y]
dy = spatial.Delaunay(points2d)
vo = spatial.Voronoi(points2d)
#%fig=德劳内三角形的外接圆与圆心
cx, cy = vo.vertices.T
ax = pl.subplot(aspect="equal")
fig = spatial.voronoi_plot_2d(vo)
#spatial.delaunay_plot_2d(dy, ax=ax)
ax.plot(cx, cy, "r.")
for i, (cx, cy) in enumerate(vo.vertices):
    px, py = points2d[dy.simplices[i, 0]]
    radius = np.hypot(cx- px, cy- py)
    circle = pl.Circle((cx, cy), radius, fill=False, ls="dotted")
    ax.add_artist(circle)
ax.set_xlim(0, 300)
ax.set_ylim(0, 300)
pl.show()
