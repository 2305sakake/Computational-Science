import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from itertools import combinations
import matplotlib.collections as clt

n = 300 # Number of Particles
h = 0.005 # Step size 
m = 1. # Mass of each particle
radius = 0.003
frames = 400

particles = np.arange(n)
particle_pairs = np.asarray(list(combinations(particles, 2)))

r = np.random.random((2,n)) # x,y positions of each particle
ixr = r[0] > 0.5; ixl = r[0] <= 0.5 # Splits particles into ones on the left and right

v = np.zeros((2,n)) 
vi = 3
v[0][ixr] = -vi; v[0][ixl] = vi

varray = np.linspace(0, vi*4, 1000) 
a = 2/vi**2
fv = a*varray*np.exp(-a*varray**2 / 2) # Theoretical Maxwell-Boltzmann Distribution

def calculate_motion(r,v):
    rs = np.zeros((frames,2,n)) # History of all position vectors for each frame
    vs = np.zeros((frames,2,n)) # History of all velocity vectors for each frame

    rs[0] = r.copy(); vs[0] = v.copy()
    for i in range(1, frames):
        handle_collision(r,v)
        handle_wall_collision(r,v)

        r += v*h

        rs[i] = r.copy(); vs[i] = v.copy()
    return rs, vs


def handle_collision(r,v):
    dx_pairs = np.diff(np.asarray(list(combinations(r[0], 2)))).ravel() # x distance between each pair
    dy_pairs = np.diff(np.asarray(list(combinations(r[1], 2)))).ravel() # y distance between each pair
    d_pairs = np.sqrt(dx_pairs**2 + dy_pairs**2) # distance between each pair
    id_pairs_collide = particle_pairs[d_pairs < 2*radius] # array of pairs that collided
    for i, j in id_pairs_collide:
        vinew=v[:,i]-(r[:,i]-r[:,j])*(2*m*np.dot(v[:,i]-v[:,j],r[:,i]-r[:,j]))/(2*m*np.linalg.norm(r[:,i]-r[:,j])**2)
        v[:,j]=v[:,j]-(r[:,j]-r[:,i])*(2*m*np.dot(v[:,j]-v[:,i],r[:,j]-r[:,i]))/(2*m*np.linalg.norm(r[:,i]-r[:,j])**2)
        v[:,i]=vinew

def handle_wall_collision(r,v):
    v[0,r[0]<radius]   = -v[0,r[0]<radius]
    v[0,r[0]>1-radius] = -v[0,r[0]>1-radius]
    v[1,r[1]<radius]   = -v[1,r[1]<radius]
    v[1,r[1]>1-radius] = -v[1,r[1]>1-radius]

def animate(i):
    ax1.cla(); ax2.cla()
    r = rs[i]; v = vs[i]
    circles = [Circle((xi,xy), radius = radius, color = 'b') for xi, xy in zip(r[0],r[1])]
    circlescollection = clt.PatchCollection(circles, match_original = True)
    ax1.add_collection(circlescollection)

    ax2.set_xlabel('Velocity'); ax2.set_ylabel('Probability')
    ax2.axis([0,vi*4,0,0.5])
    ax2.hist([np.linalg.norm(v[:,i]) for i in particles], bins = 15, density = True) 
    ax2.plot(varray,fv)

fig, (ax1, ax2) = plt.subplots(1,2)
ax1.set_aspect('equal'); 
ax2.set_box_aspect(1)

plt.tight_layout()

rs, vs = calculate_motion(r,v)

anim = FuncAnimation(fig, animate, frames, interval = h*1000)

if __name__ == '__main__':
    plt.show()