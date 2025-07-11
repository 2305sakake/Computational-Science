import numpy as np
import matplotlib.pyplot as plt

n = 10000 # Number of sites
it = 1000000 # Number of iterations

sites = np.ones(n, dtype = int) # Array of ones for each site

for _ in range(it):
    site1 = np.random.randint(n)
    if sites[site1] != 0: # Prevents having sites with negative values
        site2 = np.random.randint(n)
        sites[site1] -= 1
        sites[site2] += 1

# Plot a normalized histogram of final distribution
plt.hist(sites, bins=np.arange(-0.5, 12.5, 1), edgecolor = 'black', density = True)

# Plot theoretical Boltzmann distribution
xs = np.linspace(0,12,1000)
ys = np.log(2)*np.exp(-xs*np.log(2))
plt.plot(xs,ys)

plt.xlabel("Units of Energy")
plt.ylabel("Fraction of Total Sites")
plt.title("Experimental Energy Distribution vs Boltzmann Distribution")
plt.show()