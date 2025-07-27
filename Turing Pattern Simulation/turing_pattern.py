import numpy as np
import matplotlib.pyplot as plt

N = 256 # Grid size
Du, Dv = 0.16, 0.08 # Diffusion constants
F, k = 0.06, 0.062 # Feed and kill constants
dt = 1 # Time interval
iterations = 25000 # Number of iterations

u = np.ones((N, N)); v = np.zeros((N, N))
r = 20; c = N//2
# Set a square at the center of the grid be u = 0.5 and v = 0.25 and further perturb this square with random fluctuations
u[c-r:c+r, c-r:c+r] = 0.50*np.ones((2*r,2*r)) + 0.25*np.random.rand(2*r,2*r)
v[c-r:c+r, c-r:c+r] = 0.25*np.ones((2*r,2*r)) + 0.25*np.random.rand(2*r,2*r)

def laplacian(Z):
    """
    Calculates the Laplacian operator using a finite difference approximation
    """
    return np.roll(Z,1,0) + np.roll(Z,-1,0) + np.roll(Z,1,1) + np.roll(Z,-1,1)-4*Z

for n in range(iterations):
    uvv = u*(v**2)
    # Update u and v according to the Gray-Scott equations
    u += (Du*laplacian(u) - uvv + F*(1-u))*dt
    v += (Dv*laplacian(v) + uvv - (F+k)*v)*dt

    # Update plot every 1000 iterations
    if n % 1000 == 0:
        plt.imshow(u)
        plt.title(f"Turing Pattern Simulation\nIteration: {n}")
        plt.pause(0.01)

plt.show()