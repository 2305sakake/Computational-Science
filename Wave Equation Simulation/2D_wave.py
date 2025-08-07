import numpy as np
import matplotlib.pyplot as plt

# Parameters
T = 10.0             # Total time
c = 1.0              # Wave speed
dx = 0.01            # Spatial increments (dx=dy in this case)
nx = int(1 / dx)     # Grid segments along each axis
C = 0.7              # Courant number (< root 2 for stability)
C2 = C**2
dt = C * dx / c      # Time step size
nt = int(T / dt)     # Number of time steps

# Initialize spatial grid and displacement array
x = np.linspace(0,1,nx + 1)
y = np.linspace(0,1,nx + 1)
xx, yy = np.meshgrid(x,y)
zzs = np.zeros((nx + 1,nx + 1,nt))

# Initial condition (Choose from below or make your own)
#zzs[:,:,0] = np.sin(2*np.pi*xx)*np.sin(2*np.pi*yy)
#zzs[:,:,0] = np.exp(-100*((xx-0.5)**2+(yy-0.5)**2))
zzs[:,:,0] = np.exp(-100 * ((xx - 0.25)**2 + (yy - 0.25)**2)) + 0.5 * np.exp(-100 * ((xx - 0.75)**2 + (yy - 0.75)**2))

# Ensure Dirichlet BC of z = 0 along boundary
zzs[:, 0, 0] = zzs[:, -1, 0] = zzs[0, :, 0] = zzs[-1, :, 0] = 0
# Second time increment calculated assuming initial velocity is zero
zzs[1:-1,1:-1,1] = zzs[1:-1,1:-1,0] + C2 * (zzs[2:,1:-1,0] + zzs[:-2,1:-1,0] + zzs[1:-1,2:,0] + zzs[1:-1,:-2,0] - 4 * zzs[1:-1,1:-1,0])

# Calculate future z values using finite difference approximation
for i in range(nt-2):
    zzs[1:-1,1:-1,i + 2] = (
        2 * zzs[1:-1,1:-1,i + 1] - zzs[1:-1,1:-1,i] + 
        C2 * (
            zzs[2:,1:-1,i + 1] + zzs[:-2,1:-1,i + 1] + zzs[1:-1,2:,i + 1]
            + zzs[1:-1,:-2,i + 1]- 4 * zzs[1:-1,1:-1,i + 1]
        )
    )

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
zmax = np.abs(zzs).max()

# Update plot for every 3 time increments
for i in range(0,nt,3):
    ax.clear()
    ax.set_zlim(-zmax, zmax)
    ax.set_title("2D Wave Equation Simulation")
    ax.plot_surface(xx, yy, zzs[:, :, i])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.pause(dt)

plt.show()
