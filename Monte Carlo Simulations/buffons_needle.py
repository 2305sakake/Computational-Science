import numpy as np
import matplotlib.pyplot as plt

n = 500 # Number of needles

positions = np.random.uniform(-1,1,size=(2,n)) # Positions of centers of needles
angles = np.random.uniform(0,np.pi,size=(1,n)) # Tilt angles of needles from the horizontal

touching = 0 # Number of needles touching the line y = 0

xs = np.zeros((2,n)) # Stores x positions of the two ends of each needle
ys = np.zeros((2,n)) # Stores y positions of the two ends of each needle

# Iterate through each needle and calculate positions of two ends of needle
for i in range(n):
   position = positions[:,i]
   angle = angles[0,i]
   x1 = position[0] - np.cos(angle); x2 = position[0] + np.cos(angle)
   y1 = position[1] - np.sin(angle); y2 = position[1] + np.sin(angle)
   xs[:,i] = [x1,x2] # Add x positions to xs array
   ys[:,i] = [y1,y2] # Add y positions to ys array
   if y1 <= 0 <= y2:  # Needle touching y = 0
      touching += 1

pi = 2*n/touching # Calculate approximate value for pi

# Plot needles and y = 0 line
fig, ax = plt.subplots()
plt.plot([-2,2],[0,0],'k',linewidth=1.5)
plt.plot(xs,ys,linewidth = 0.75)
plt.text(1.2,2.35,f"Touching needles: {touching}")
plt.text(1.2,2.15,f"Calculated pi: {pi:.8f}")
ax.set_xlim([-2,2])
ax.set_ylim([-2,2])
ax.set_aspect('equal')
plt.show()
