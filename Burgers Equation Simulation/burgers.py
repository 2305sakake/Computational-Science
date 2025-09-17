import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

nx = 512         # Spatial segments
L = 2 * np.pi    # Length of domain
dx = L / nx      # Spatial increment
nu = 0.01        # Viscosity
T = 7.0          # Total time
dt = 0.001       # Time step
nt = int(T / dt) # Total temporal increments

k = np.fft.fftfreq(nx, d=dx) * 2 * np.pi # Wave number

# Set up spatial and temporal arrays
xs = np.linspace(0, L, nx, endpoint=False)
ts = np.linspace(0, T, nt)

# Initial wave speed
u0 = np.exp(-(xs - 2) ** 2)

def burgers(u, t, k, nu):
    """Defines ODE resulting from performing Fourier tranform on Burgers' equation"""
    # Transform to Fourier transform basis and calculate derivatives
    u_hat = np.fft.fft(u)
    u_hat_x = 1j * k * u_hat
    u_hat_xx = -k ** 2 * u_hat

    # Inverse transform back and calculate RHS of Burgers' equation
    u_x = np.fft.ifft(u_hat_x)
    u_xx = np.fft.ifft(u_hat_xx)
    u_t = -u * u_x + nu * u_xx

    return u_t.real

solution = odeint(burgers, u0, ts, args=(k, nu))

fig, ax = plt.subplots()
line, = ax.plot(xs, solution[0], lw=2)
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, ha="left", va="top")

ax.set_ylim(-0.1, 1.1)
ax.set_xlim(0, L)
ax.set_xlabel("x")
ax.set_ylabel("Wave speed, u")
ax.set_title("1D Burgers' Equation Simulation")

def animate(frame):
    """Function ran every frame and updates plot to create animation"""
    line.set_ydata(solution[frame])
    time_text.set_text(f"t = {ts[frame]:.3f} s")
    return line, time_text

animation = FuncAnimation(fig, animate, frames=nt, blit=True, interval=dt*1000, repeat=False)

plt.show()
