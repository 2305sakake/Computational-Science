import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Define constants
h = 0.01 # Step size
m1 = 1.; m2 = 1.
L1 = 1.; L2 = 1.; g = 9.81
Lt = L1 + L2 + 0.2
phi1 = np.pi/3; phi2 = np.pi; w1 = 0; w2 = 0

# Define state array with initial conditions 
y = np.array([phi1, phi2, w1, w2])

def f(y):
    """Derivatives of each component of y"""
    s = np.sin(y[0]-y[1]); c = np.cos(y[0]-y[1])
    tm = m1 + m2; denom = L1*(2*m1+m2-m2*np.cos(2*(y[0]-y[1])))
    f2 = (-g*(2*m1+m2)*np.sin(y[0]) - m2*g*np.sin(y[0]-2*y[1])-2*s*m2*(y[3]**2*L2+y[2]**2*L1*c))/denom
    f3 = (2*s*(y[2]**2*L1*tm+g*tm*np.cos(y[0])+y[3]**2*L2*m2*c))/denom
    return np.array([y[2],y[3],f2,f3])

def rk4(y):
    """ODE solver using the rk4 method"""
    k1 = h*f(y)
    k2 = h*f(y+k1/2.)
    k3 = h*f(y+k2/2.)
    k4 = h*f(y+k3)
    y = y + (k1 + 2.*(k2 + k3) + k4)/6.
    return y

# Set up matplotlib plots
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.axis([-Lt, Lt, -Lt, Lt])
ax2.axis([-np.pi, np.pi, -np.pi, np.pi])
ax1.set_aspect('equal'); ax2.set_aspect('equal')

line, = ax1.plot([], [], 'o-') # Used for double pendulum
trace, = ax2.plot([], []) # Used for tracing the path in configuration space
time_template = 'time = %.1fs'
time_text = ax1.text(0.05, 0.9, '', transform=ax1.transAxes)

history1 = np.array([y[0]]); history2 = np.array([y[1]])

def animate(i):
    """Function that is ran every frame and updates plots according to the rk4 solution"""
    global y; global history1; global history2
    y = rk4(y)

    history1 = np.append(history1, (y[0]+np.pi)%(2*np.pi)-np.pi)
    history2 = np.append(history2, (y[1]+np.pi)%(2*np.pi)-np.pi)

    x1 = L1*np.sin(y[0]); y1 = -L1*np.cos(y[0])
    x2 = x1 + L2*np.sin(y[1]); y2 = y1 - L2*np.cos(y[1])

    line.set_data([0, x1, x2],[0, y1,y2])
    trace.set_data(history1[:i], history2[:i])
    time_text.set_text(time_template % (i*h))

    return line, trace, time_text

anim = FuncAnimation(fig, animate, 10000, interval = h*1000, blit = True)
plt.show()
