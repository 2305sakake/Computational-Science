import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

# Read in data using pandas
df = pd.read_csv('./astmg173.csv', skiprows = 1)
wavelength = df['Wvlgth nm'].values*1e-9
irradiance = df['Etr W*m-2*nm-1'].values

# Smooth noise using Savitzky-Golay filter
irradiance = savgol_filter(irradiance, window_length=31, polyorder=3)

# Define necessary constants for Planck's law
h = 6.626e-34
c = 3e8
k = 1.381e-23

def planck_law(wavelength, T, a):
    """Function that defines Planck's law"""
    return a * (8 * np.pi * h * c) / (wavelength**5) / (np.exp((h * c) / (wavelength * k * T)) - 1)

# Fit data against Planck's law using scipy's curve_fit
popt, pcov = curve_fit(planck_law, wavelength, irradiance, p0=[5500,1])
perr = np.sqrt(np.diag(pcov)) # Errors for each parameter extracted from the covariance matrix
T_fit, T_fit_err = popt[0], perr[0]
print(f"Fitted temperature: {T_fit:.2f} K")
print(f"Fitted temperature error: {T_fit_err:.2f} K")

# Plot data and fitted curve
plt.plot(wavelength * 1e9, irradiance)
plt.plot(wavelength * 1e9, planck_law(wavelength,T_fit,popt[1]))
plt.xlabel('Wavelength (nm)')
plt.ylabel('Irradiance (W/m²/nm)')
plt.title('Experimental vs Fitted Blackbody Curve')
plt.tight_layout()
plt.show()
