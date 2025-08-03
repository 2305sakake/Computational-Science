import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# --- Parameters ---
T1 = 250.0             # Total simulation time for phase space plot
T2 = 100000.0          # Total simulation time for Poincare section
delta = 0.1            # Duffing oscillator parameters
alpha = -1.0
beta = 0.25
gamma = 2.5
omega = 2.0

dt = 0.001             # Time step for phase space plot
Td = 2 * np.pi / omega # Driving period

state1 = (1, 0)      # Initial conditions (x, v)
state2 = (1.0001, 0) # Same initial condition but with tiny pertubation

t1 = np.arange(0, T1, dt) # Time array for phase space plot
t2 = np.arange(0, T2, Td) # Time array for Poincare section

# Duffing equation
def duffing(state, t, delta, alpha, beta, gamma, omega):
    x, v = state
    return [v, gamma * np.cos(omega * t) - (delta * v + alpha * x + beta * x**3)]

# Solve ODE for t1 and t2 array
evolution1 = odeint(duffing, state1, t1, args=(delta, alpha, beta, gamma, omega))
evolution2 = odeint(duffing, state2, t1, args=(delta, alpha, beta, gamma, omega))
poincare_evolution = odeint(duffing, state1, t2, args=(delta, alpha, beta, gamma, omega))

# Set up plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plotting phase space trajectory
ax1.plot(evolution1[:,0],evolution1[:,1], lw=0.75)
ax1.plot(evolution2[:,0],evolution2[:,1], lw=0.75)
ax1.set_title(f"Duffing Oscillator Phase Space Trajectory\n(δ={delta},α={alpha}, β={beta}, γ={gamma}, ω={omega})")
ax1.set_xlabel("x")
ax1.set_ylabel("v")

# Plotting poincare section
ax2.scatter(poincare_evolution[:,0], poincare_evolution[:,1], s=0.5, c='black')
ax2.set_title(f"Poincaré Section of Duffing Oscillator\n(δ={delta}, α={alpha}, β={beta}, γ={gamma}, ω={omega})")
ax2.set_xlabel("x")
ax2.set_ylabel("v")

plt.tight_layout()
plt.show()
