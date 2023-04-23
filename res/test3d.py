import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

from mpl_toolkits.mplot3d.axes3d import get_test_data


fig = plt.figure(figsize=plt.figaspect(0.5))

ax0 = fig.add_subplot(1, 2, 1, projection='3d')
ax1 = fig.add_subplot(1, 2, 2, projection='3d')

x = np.arange(0., 1.1, 0.1)
y = np.arange(0.0, .11, 0.01)

X, Y = np.meshgrid(x, y)

z1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
               [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
               [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

z2 = np.array([[1485.22, 1474.94, 1485.1, 1486.62, 1487.78, 1489.1, 1489.56, 1485.46, 1482.72, 1483.08, 1481.76],
               [1486.28, 1493.4, 1488.88, 1490.32, 1487.58, 1488.64, 1487.48, 1487.54, 1491.36, 1486.76, 1489.72],
               [1475.84, 1485.24, 1490.74, 1490.72, 1492.46, 1487.84, 1490.14, 1487.72, 1491.8, 1481.38, 1491.3],
               [1483.64, 1486.6, 1488.62, 1489.06, 1484.16, 1484.16, 1492.06, 1485.56, 1491.78, 807.08, 642.54],
               [1490.52, 1488.34, 1482.98, 1490.34, 1487.28, 1488.76, 1486.84, 949.38, 668.06, 556.2, 491.2, ],
               [1489.36, 1490.02, 1491.16, 1485.98, 1493.66, 1490.5, 740.68, 569.44, 484.62, 430.7, 391.52],
               [1486.42, 1486.7, 1481., 1484.82, 1488.42, 637.12, 494.4, 424.08, 380.26, 353.78, 323., ],
               [1487.5, 1494.16, 1490.02, 1047.86, 556.14, 439.86, 372.22, 332.3, 296.02, 279.68, 261.24],
               [1486.5, 1481.14, 994.48, 497.8, 376.04, 317.78, 281.06, 255.02, 234.7, 224.3, 210.34],
               [1488.14, 1097.88, 424.1, 311.06, 264., 232.28, 209.6, 191.18, 178.32, 172.1, 160.1, ],
               [1492.78, 319.56, 220.18, 192.36, 157.08, 143.42, 137.22, 130.52, 127.78, 117.2, 117.24]])

ax0.plot_wireframe(X, Y, z1, rstride=1, cstride=1)
ax0.set_zlim(0, 1)

surf = ax1.plot_surface(X, Y, z2, rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=1, shade=False, alpha=0.6)

fig.colorbar(surf, extend="max", location="bottom")


ax0.set_zlim([0, 1])
ax0.set_xlabel('coupling'), ax0.set_ylabel(r'$\delta_2$'), ax0.set_zlabel('Response rate %')
ax0.set_title('response rate')

#
ax1.set_xlabel('coupling'), ax1.set_ylabel(r'$\delta_2$'), ax1.set_zlabel(r'avg response time (t $\cdot$ dt)')
ax1.set_title('Average response time')

ax1.view_init(20, -20)
ax0.view_init(20, -70)


plt.tight_layout()
plt.show()
