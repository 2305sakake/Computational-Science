from vpython import *
import numpy as np

# Define constants and initial conditions
t, tf = 0.0, 1000.0 # Start and end time
h = 0.05 # Step size
a = 0.1 # Factor for precession due to general relativity

m1, m2, m3 = 1.0, 1.0, 10.0
r1, v1 = np.array([10.0, 0.0, 0.0]), np.array([-0.2, 0.0, 0.1]) # Initial conditions for body 1
r2, v2 = np.array([-10.0, 0.0, 0.0]), np.array([0.0, 0.1, -0.1]) # Initial conditions for body 2
r3, v3 = np.array([0.0, 0.0, 5.]), np.array([0.2, -0.1, 0.0]) # Initial conditions for body 3
y = np.concatenate((r1,r2,r3,v1,v2,v3)) # State array

def f(y):
    """Derivatives of each component of y"""
    r12 = ((y[0] - y[3])**2 + (y[1] - y[4])**2 + (y[2] - y[5])**2)**(1 / 2) # Relative distance between 1 and 2
    r23 = ((y[3] - y[6])**2 + (y[4] - y[7])**2 + (y[5] - y[8])**2)**(1 / 2) # Relative distance between 2 and 3
    r31 = ((y[6] - y[0])**2 + (y[7] - y[1])**2 + (y[8] - y[2])**2)**(1 / 2) # Relative distance between 3 and 1
    return np.concatenate((y[9:18],
                m2 * (y[3:6] - y[0:3]) / r12**(3 + a) + m3 * (y[6:9] - y[0:3]) / r31**(3 + a),
                m1 * (y[0:3] - y[3:6]) / r12**(3 + a) + m3 * (y[6:9] - y[3:6]) / r23**(3 + a),
                m1 * (y[0:3] - y[6:9]) / r31**(3 + a) + m2 * (y[3:6] - y[6:9]) / r23**(3 + a)))

def rk4(y):
    """ODE solver using the rk4 method"""
    k1 = h * f(y)
    k2 = h * f(y + k1 / 2.0)
    k3 = h * f(y + k2 / 2.0)
    k4 = h * f(y + k3)
    return y + (k1 + 2.0 * (k2 + k3) + k4) / 6.0

# Set up vPython canvas and objects
scene = canvas(x=0, y=0, width=700, height=700)

path1 = curve(color = color.blue, radius = 0.13)
path2 = curve(color = color.red, radius = 0.13)
path3 = curve(color = color.green, radius = 0.13)

body1 = sphere(pos = vec(r1[0],r1[1],r1[2]), color = color.blue, radius = 0.5)
body2 = sphere(pos = vec(r2[0],r2[1],r2[2]), color = color.red, radius = 0.5)
body3 = sphere(pos = vec(r3[0],r3[1],r3[2]), color = color.green, radius = 0.5)

# While loop that repeatedly runs rk4 and updates the vPython objects
while t < tf:
    rate(500) # 500 times per second
    y = rk4(y)
    t += h

    # Update position of bodies
    body1.pos = vec(y[0], y[1], y[2])
    body2.pos = vec(y[3], y[4], y[5])
    body3.pos = vec(y[6], y[7], y[8])

    # Append paths with new positions of bodies
    path1.append(pos = vec(y[0], y[1], y[2]))
    path2.append(pos = vec(y[3], y[4], y[5]))
    path3.append(pos = vec(y[6], y[7], y[8]))
