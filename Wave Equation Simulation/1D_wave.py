import numpy as np
import matplotlib.pyplot as plt

# Parameters
T = 10.0         # Total time
c = 1.0          # Wave speed
dx = 0.01        # Spatial increments
nx = int(1 / dx)   # Number of segments on string
C = 0.99         # Courant number (< 1 for stability)
C2 = C**2 
dt = C * dx / c      # Time step size
nt = int(T / dt)   # Number of time steps

# Initialize spatial grid and displacement array
x = np.linspace(0,1,nx + 1)
ys = np.zeros((nx + 1,nt))

# Initial condition (Choose from below or make your own)
#ys[:,0] = np.sin(2*np.pi*x)
ys[nx // 2 - 10:nx // 2 + 10,0] = np.exp(-500 * (x[nx // 2 - 10:nx // 2 + 10] - 0.5)**2)

# Second time increment calculated assuming initial velocity is zero
ys[1:-1, 1] = ys[1:-1, 0] + 0.5 * C2 * (ys[2:, 0] - 2 * ys[1:-1, 0] + ys[:-2, 0])

# Calculate future y values using finite difference appproximation
for i in range(nt-2):
    ys[1:-1,i + 2] = 2 * ys[1:-1,i + 1] - ys[1:-1,i] + C2 * (ys[2:,i + 1] - 2 * ys[1:-1,i + 1] + ys[:-2,i + 1])

# Set up plot
fig, ax = plt.subplots()
line, = ax.plot(x, ys[:, 0])
max_amp = np.max(np.abs(ys))
ax.set_ylim(-1.1 * max_amp, 1.1 * max_amp)
ax.set_title("1D Wave Equation Simulation")

# Plot wave
for i in range(nt - 1):
    line.set_ydata(ys[:, i + 1])
    plt.pause(dt)

plt.show()
