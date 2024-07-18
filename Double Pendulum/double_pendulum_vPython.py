from vpython import *
import numpy as np

# Define time bounds and step size h
t = 0.; tf = 100.
h = 0.01

# Define constants
m1 = 1.; m2 = 1.
L1 = 1.; L2 = 1.; g = 9.81
phi1 = pi/3; phi2 = pi; w1 = 0; w2 = 0

# Define state array with initial conditions 
y = np.array([phi1, phi2, w1, w2])

def f(y):
    """Derivatives of each component of y"""
    s = sin(y[0]-y[1]); c = cos(y[0]-y[1])
    tm = m1 + m2; denom = L1*(2*m1+m2-m2*cos(2*(y[0]-y[1])))
    f2 = (-g*(2*m1+m2)*sin(y[0]) - m2*g*sin(y[0]-2*y[1])-2*s*m2*(y[3]**2*L2+y[2]**2*L1*c))/denom
    f3 = (2*s*(y[2]**2*L1*tm+g*tm*cos(y[0])+y[3]**2*L2*m2*c))/denom
    return np.array([y[2],y[3],f2,f3])

def rk4(y):
    """ODE solver using the rk4 method"""
    k1 = h*f(y)
    k2 = h*f(y+ k1/2.)
    k3 = h*f(y+k2/2.)
    k4 = h*f(y+k3)
    y = y + (k1 + 2.*(k2 + k3) + k4)/6.
    return y


# Set up vPython canvas
scene = canvas(x=0,y=0,width = 600, height = 600, center = vec(0,-(L1+L2)/2,0), range = L1+L2+0.2, align='left')

# Set up graph and curve to plot phi1 vs phi2
graph = graph(x=0,y=0,width = 600, height = 600, title = 'Configuration Space',
               xtitle = 'phi1', ytitle = 'phi2', xmin=-pi, xmax=pi, ymin=-pi, ymax=pi, align='left')
funct = gcurve(color = color.blue)

def plotconfig():
    """Updates canvas with current positions of spheres and lines"""
    for obj in scene.objects:
        obj.visible = 0 # Removes previous configuration of objects

    x1 = L1*sin(y[0]); y1 = -L1*cos(y[0]) # x,y position of first ball
    x2 = x1 + L2*sin(y[1]); y2 = y1 - L2*cos(y[1]) # x,y position of second ball

    sphere(pos=vec(x1, y1, 0), color=color.cyan, radius= 0.1)
    sphere(pos=vec(x2, y2, 0), color=color.cyan, radius= 0.1)
    curve(pos=[vec(0, 0, 0), vec(x1,y1, 0)], color=color.yellow, radius=0.025)
    curve(pos=[vec(x1, y1, 0), vec(x2,y2, 0)], color=color.yellow, radius=0.025)

# While loop that repeatedly solves the ODEs and updates the canvas
while t < tf:
    rate(100) # 100 times per second
    y = rk4(y)
    t += h
    plotconfig()
    funct.plot(pos = ((y[0]+pi)%(2*pi)-pi, (y[1]+pi)%(2*pi)-pi)) # Trace path in configuration space