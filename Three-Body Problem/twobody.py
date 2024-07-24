from vpython import *
import numpy as np

# Define constants and initial conditions
t = 0.; tf = 1000. # Start and end time
h = 0.05 # Step size
a = 0.1 # Factor for precession due to general relativity

m1 = 1; m2 = 10
r1 = np.array([10,0]); v1 = np.array([0, 0.3]) # Initial conditions for body 1
r2 = np.array([0,0]);  v2 = np.array([0,-0.03]) # Initial conditions for body 2
y = np.concatenate((r1, r2, v1, v2)) # State array

def f(y):
    """Derivatives of each component of y"""
    r = ((y[0]-y[2])**2+(y[1]-y[3])**2)**(1/2) # Relative distance
    return np.concatenate((y[4:8],
            m2*(y[2:4]-y[0:2])/r**(3+a),
            m1*(y[0:2]-y[2:4])/r**(3+a)))

def rk4(y):
    """ODE solver using the rk4 method"""
    k1 = h*f(y)
    k2 = h*f(y+k1/2.)
    k3 = h*f(y+k2/2.)
    k4 = h*f(y+k3)
    return y + (k1 + 2.*(k2 + k3) + k4)/6.

# Set up vPython graph and curves
graph = graph(x=0,y=0,width = 400, height = 400, xtitle = 'x', ytitle = 'y',
              xmin=-15, xmax=15, ymin=-15, ymax=15)

path1 = gcurve(color = color.blue) # Path of body 1
path2 = gcurve(color = color.red) # Path of body 2

# While loop that repeatedly runs rk4 and updates graphs
while t < tf:
    rate(300) # 300 times per second
    y = rk4(y)
    t += h

    # Update graphs
    path1.plot(pos = (y[0], y[1]))
    path2.plot(pos = (y[2], y[3]))