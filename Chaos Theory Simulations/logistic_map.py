import numpy as np
import matplotlib.pyplot as plt

# --- Parameters ---
r_min = 2.0      # Minimum value of r
r_max = 4.0      # Maximum value of 4
r_step = 0.0001  # Step size in r
N = 1000          # Number of iterations to skip during transient phase
n = 100          # Number of iterations to plot during steady state

# Initialize array for r and x values
rs = np.arange(r_min, r_max, r_step) 
xs = np.empty((len(rs), n))

# Loop over each r value
for i, r in enumerate(rs):
    x = 0.5 # Initial condition

    # Let system evolve to skip transient phase
    for _ in range(N):
        x = r * x * (1 - x)

    # Store values for steady state
    for j in range(n):
        x = r * x * (1 - x)
        xs[i,j] = x

# ---Plotting---
plt.figure(figsize=(10, 7))
plt.title("Bifurcation Diagram of the Logistic Map", fontsize=16)
plt.xlabel("r", fontsize=14)
plt.ylabel("x", fontsize=14)
plt.tight_layout()

plt.plot(np.repeat(rs, n), xs.flatten(), ',k', alpha=0.5)

plt.show()