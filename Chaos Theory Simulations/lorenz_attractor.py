import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.animation import FuncAnimation

# --- Parameters ---
T = 100.0 # Total time
h = 0.01  # Time step
sigma, rho, beta = 10.0, 28.0, 2.7 # Lorenz system parameters
r1 = (1, 0, 10)     # Initial position
r2 = (1, 0, 10.001) # Same initial position but with small pertubation

t = np.arange(0, T, h)

# Lorenz system function
def lorentz(r, t, sigma, rho, beta):
    x, y, z = r
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

# Integrate trajectories
evolution1 = odeint(lorentz, r1, t, args=(sigma, rho, beta))
evolution2 = odeint(lorentz, r2, t, args=(sigma, rho, beta))

# Set up plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_title(f"Lorenz Attractor of Two Particles with Nearly Identical Initial Conditions\n(σ={sigma}, ρ={rho}, β={beta})", fontsize=14)
ax.set_xlim(-25, 25)
ax.set_ylim(-35, 35)
ax.set_zlim(0, 50)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

line1, = ax.plot([], [], [], lw=0.75, color='blue', )
line2, = ax.plot([], [], [], lw=0.75, color='red')

# Update function for animation
def update(frame):
    line1.set_data(evolution1[:frame, 0], evolution1[:frame, 1])
    line1.set_3d_properties(evolution1[:frame, 2])
    
    line2.set_data(evolution2[:frame, 0], evolution2[:frame, 1])
    line2.set_3d_properties(evolution2[:frame, 2])

    return line1, line2

# Create animation
frames = len(t)
ani = FuncAnimation(fig, update, frames=frames, interval=10, blit=True)

plt.tight_layout()
plt.show()