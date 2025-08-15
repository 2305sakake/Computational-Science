from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
import matplotlib.collections as clt

n = 300 # Number of Particles
h = 0.005 # Step size
m = 1.0 # Mass of each particle
radius = 0.004
frames = 300

# Give labels to each particle and pairs of particles
particles = np.arange(n)
particle_pairs = np.asarray(list(combinations(particles, 2)))

r = np.random.random((2,n)) # x,y positions of each particle
ixr, ixl = r[0] > 0.5, r[0] <= 0.5 # Splits particles into ones on the left and right

# Initial Velocity
v = np.zeros((2,n))
vi = 3
v[0][ixr], v[0][ixl] = vi, -vi

def calculate_motion(r,v):
    """Calculates the motion of particles for all frames"""
    rs = np.zeros((frames,2,n)) # History of all position vectors for each frame
    vs = np.zeros((frames,2,n)) # History of all velocity vectors for each frame

    rs[0], vs[0] = r.copy(), v.copy()
    for i in range(1, frames):
        handle_collision(r,v)
        handle_wall_collision(r,v)

        r += v * h

        rs[i], vs[i] = r.copy(), v.copy()
    return rs, vs


def handle_collision(r,v):
    """Detects whether collisions have occured between particles and changes velocities accordingly"""

    # x and y distance between each pair
    dx_pairs = np.diff(np.asarray(list(combinations(r[0], 2)))).ravel()
    dy_pairs = np.diff(np.asarray(list(combinations(r[1], 2)))).ravel()

    # Distance between each pair
    d_pairs = np.sqrt(dx_pairs**2 + dy_pairs**2)

    # Array of pairs that collided
    particle_pairs_collide = particle_pairs[d_pairs < 2*radius]

    for i, j in particle_pairs_collide:
        vinew = v[:,i] - (r[:,i] - r[:,j]) * (2 * m * np.dot(v[:,i] - v[:,j], r[:,i] - r[:,j])) / (2 * m * np.linalg.norm(r[:,i] - r[:,j])**2)
        v[:,j] = v[:,j] - (r[:,j] - r[:,i]) * (2 * m * np.dot(v[:,j] - v[:,i], r[:,j] - r[:,i])) / (2 * m * np.linalg.norm(r[:,i] - r[:,j])**2)
        v[:,i] = vinew

def handle_wall_collision(r,v):
    """Detects whether collisions have occured with wall and changes velocities accordingly"""
    v[0, r[0] < radius] = -v[0,r[0] < radius]
    v[0, r[0] > 1 - radius] = -v[0, r[0] > 1 - radius]
    v[1, r[1] < radius] = -v[1, r[1] < radius]
    v[1, r[1] > 1 - radius] = -v[1, r[1] > 1 - radius]

rs, vs = calculate_motion(r,v)

# Set up theoretical Maxwell-Boltzmann Distribution
varray = np.linspace(0, vi * 4, 1000)
a = 2 / vi**2
fv = a*varray*np.exp(-a * varray**2 / 2)

# Set up plot
fig, (ax1, ax2) = plt.subplots(1,2)
fig.suptitle(f"{n } Particle Gas Simulation and \nComparison with Maxwell-Boltzmann Distribution", fontsize=14)
ax1.set_aspect('equal')
ax2.set_box_aspect(1)
circles = [Circle((xi, yi), radius=radius, color='b') for xi, yi in zip(r[0], r[1])]
circlescollection = clt.PatchCollection(circles, match_original=True)
ax1.add_collection(circlescollection)
plt.tight_layout()

def animate(i):
    """Function ran every frame and updates plot to create animation"""
    r, v = rs[i], vs[i]
    
    for circle, (xi, yi) in zip(circles, zip(r[0], r[1])):
        circle.center = (xi, yi)  # update position only
    circlescollection.set_paths(circles)
    
    ax2.cla()
    ax2.set_xlabel('Velocity')
    ax2.set_ylabel('Probability')
    ax2.axis([0, vi * 4, 0, 0.5])
    ax2.hist([np.linalg.norm(v[:, j]) for j in particles], bins=15, density=True)
    ax2.plot(varray, fv)
    
    return [circlescollection]

anim = FuncAnimation(fig, animate, frames, interval = h*1000)

plt.show()
