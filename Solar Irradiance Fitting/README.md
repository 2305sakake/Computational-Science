# Solar Irradiance Fitting

## Overview

This is a program that takes real solar irradiance data and fits it to the known black body curve governed by Planck's law. The data used comes from The National Renewable Energy Laboratory (NREL) and the csv file is included in the folder. From the fitting process, an estimated temperature of the Sun of (5498.47 +/- 8.40) K is calculated in comparison to the accepted value of 5772 K. While our result is not quite consistent with the accepted value, given the limitations in the data (particulary the large fluctuations for wavelengths below 1000 nm), and the likelihood of some sort of systematic error, a percent error of 4.7% is acceptable. A brief explanation of the program is given below.

## Details

This is a relatively standard curve fitting program and works by first reading in the csv file using pandas, defining a function for the theoretical equation, and fitting the data to the function using scipy's curve_fit. A few things that should be noted however, is that first of all, since the raw data was quite noisy I used a Savitsky_Golay filter to produced a smoother curve for the irradiance. Secondly, I had to include an extra scaling parameter, a, to the fit to account for attenuation in the irradiance as a result of atmospheric absorption and other factors. 

# Reference

Reference Air Mass 1.5 Spectra | Grid Modernization | NREL. (2025). Nrel.gov. https://www.nrel.gov/grid/solar-resource/spectra-am1.5

‌