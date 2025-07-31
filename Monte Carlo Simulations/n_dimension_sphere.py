import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

n = 3 # Number of dimensions
N = 100000 # Number of points
points = np.random.uniform(-1,1,(n,N)) # Random array of points
inside = [] # Points that are inside the sphere

for i in range(N):
    point = points[:,i]
    if np.linalg.norm(point) < 1: # If norm is less than one then inside sphere
        inside.append(point)

# Convert lists into numpy arrays
inside = np.array(inside).T if inside else np.empty((n, 0))

cvolume = (2**n) * inside.shape[1] / N # Computed volume from Monte Carlo integration
tvolume = np.pi**(n / 2) / (gamma(n / 2 + 1)) # Theoretical volume

print(f"Computed volume = {cvolume}")
print(f"Theoretical volume = {tvolume}")
