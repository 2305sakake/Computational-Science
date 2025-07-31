import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.animation import FuncAnimation

h = 0.0005

x1 = 7.; v1 = -3.; m1 = 100**(1); l1 = m1**(1/10)
x2 = 3.; v2 = 0.; m2 = 1; l2 = 1
collisions = 0

v1_history = np.array([m1**(1/2)*v1]); v2_history = np.array([v2])
radius = abs(m1**(1/2)*v1)
ax_lim = 1.1*radius

def detect_collision():
    global v1; global v2
    d = x1 - x2 #distance between bottom left corners of masses

    if x2 <= 0: # Mass 2 collides with left wall
        v2 = -v2 
        return True
    if d <= l2: # Mass 1 and 2 collide with each other
        v1_new = (2*m2*v2+(m1-m2)*v1)/(m1+m2)
        v2 = (2*m1*v1-(m1-m2)*v2)/(m1+m2)
        v1 = v1_new
        return True

def animate(i):
    global x1; global x2; global collisions; global v1_history; global v2_history

    if detect_collision():
        collisions += 1
        v1_history = np.append(v1_history, m1**(1/2)*v1)
        v2_history = np.append(v2_history, v2)
        lines.set_data(v1_history, v2_history)
        collisions_text.set_text(f"Number of collisions: {collisions}")

    x1 += v1 * h; x2 += v2 * h

    block1.set_x(x1); block2.set_x(x2)

    return block1, block2, collisions_text, lines

fig, (ax1, ax2) = plt.subplots(1,2)
ax1.axis([0,10,0,10]); ax1.set_aspect('equal')
ax2.axis([-ax_lim, ax_lim, -ax_lim, ax_lim]); ax2.set_aspect('equal')
ax2.set_xlabel(r'$\sqrt{m_1}v_1$'); ax2.set_ylabel(r'$v_2$')

block1 = Rectangle(xy = np.array([x1, 0]), width = l1, height = l1)
block2 = Rectangle(xy = np.array([x2, 0]), width = l2, height = l2)
ax1.add_patch(block1); ax1.add_patch(block2)

collisions_text = ax1.text(0.05, 0.9, f"Number of collisions: {collisions}", transform=ax1.transAxes)

energy_circle = Circle(xy = np.array([0,0]), radius = radius, fill = False)
ax2.add_patch(energy_circle)
lines, = ax2.plot(v1_history, v2_history)

plt.tight_layout()

anim = FuncAnimation(fig, animate, 1000, interval = h*1000, blit = True)
plt.show()
