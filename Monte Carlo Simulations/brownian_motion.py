import numpy as np
import matplotlib.pyplot as plt

n = 1000 # Number of steps
p = 1000 # Number of paths
t = 1.0 # End time

mu, sigma = 5.0, 2.0 # Mean and standard deviation

dt = t / n # Time increment between each step
dy = mu*dt + sigma * np.sqrt(dt) * np.random.normal(0,1,(p,n)) # Change in y for each increment

ts = np.linspace(0, t, n + 1)
ys = np.zeros((p, n + 1))

for i in range(n):
    ys[:,i + 1] = ys[:,i] + dy[:,i]

# Plot each path
fig, (ax1, ax2) = plt.subplots(1,2)
for i in range(p):
    ax1.plot(ts, ys[i,:], lw = 1)
ax1.set_box_aspect(1)

# Histogram of final values
ax2.hist(ys[:,n], bins = 25, density = True)

# Theoretical distribution of final values
xs = np.linspace(np.min(ys[:,n]),np.max(ys[:,n]),1000)
distribution = np.exp(-0.5 * ((xs - mu*t) / (sigma * np.sqrt(t)))**2) / (sigma * np.sqrt(2 * t * np.pi))
ax2.plot(xs,distribution)
ax2.set_box_aspect(1)

plt.tight_layout()
plt.show()
