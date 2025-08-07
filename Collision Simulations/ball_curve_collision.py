import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

g = 9.81 # gravitational acceleration
dt = 0.001 # time increment
frames = 20000
lwall, rwall = -2, 2
bwall, twall = -1, 4
cr = 1 # coefficient of restitution

r = np.array([1.5,3.]) # position vector
v = np.array([3.,0.]) # velocity vector

def func(x):
    """Curve over which the ball can bounce on"""
    return 2 * np.exp(-x**2)

def calculate_distance(f, r, x):
    """Calculates the distance bewteen the particle and the curve"""
    return np.hypot(x - r[0], f(x) - r[1])

def calculate_deriv(f,x):
    """Central difference algorithm for caluclating derivative"""
    h = 0.001
    return (f(x + h/2) - f(x - h/2)) / h

def handle_collision(r,v):
    """Detects whether a collision has occured and changes velocity of ball accordingly"""
    if (r[0] < lwall+0.05) or (r[0] > rwall-0.05):
        v[0] *= -cr
        v[1] *= cr
    elif r[1] < bwall + 0.05:
        v[0] *= cr
        v[1] *= -cr
    else:
        for i in range(2):
            x = r[0] + 0.01 * (-1)**i # checks x distance of 0.01 on both sides
            dist = calculate_distance(func, r, x)
            if dist < 0.05:
                deriv = calculate_deriv(func, x)
                if deriv == 0:
                    n = np.array([0,1]) # normal vector points up
                else:
                    n = np.array([1,-1/deriv])
                n = n/(n[0]**2 + n[1]**2)**(1/2) # normalize vector
                v -= 2 * cr * np.dot(v,n) * n
                break
    return v

def calculate_motion(r,v):
    """Calculates the motion of the ball for all frames"""
    rs = np.zeros((frames,2)) # history of all the position vectors for every frame
    for i in range(0, frames):
        v[1] -= g * dt
        v = handle_collision(r,v)

        r += dt * v

        rs[i] = r.copy()
    return rs

def init():
    """Initializes objects for animation"""
    return line, ball

def animate(i):
    """Function ran every frame and updates plot to create animation"""
    ball.set_center((rs[i,0],rs[i,1]))
    if trace_path:
        line.set_data(rs[:i,0],rs[:i,1])
    return line, ball

fig, ax = plt.subplots()
ax.set_xlim(lwall,rwall)
ax.set_ylim(bwall,twall)
ax.set_aspect('equal')
xs = np.arange(lwall,rwall,0.01)
ax.plot(xs,func(xs))

ball = ax.add_patch(plt.Circle((r[0],r[1]),0.05))
line, = ax.plot([], [])

trace_path = False

rs = calculate_motion(r,v)

ani = animation.FuncAnimation(fig, animate, frames = frames, repeat=False,
                               init_func=init, interval = dt*1000, blit=True)
plt.show()
