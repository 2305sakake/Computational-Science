# Three-Body Problem Simulation

## Overview

In this project, I have created a program that simulates orbital mechanics and the three-body problem on Python. Initially, I created a simplified version with only two bodies in two dimensions but later extended this to the three-body problem in three dimensions. Both versions are included in this folder. The two body version is useful for simulating basic planetary orbits whereas the three body version is able to simulate chaotic systems.

## Details

To simulate the motion of two or three masses under each other's gravity, I used the differential equations derived by Newton's universal law of gravitation to determine how the system evolves with time. These differential equations were solved using the rk4 method and the results were visually simulated on vPython.

The variable 'a' I have included is a factor that can roughly reproduce the precession that is predicted by general relativity. You can switch between a = 0 and a small non-zero value for a to see how this affects the motion of the bodies.

Also note that when running this program, the bodies can sometimes abruptly fly away from each other and this is due to the fact that the bodies get too close to each other, leading to a division by a number near 0. To fix this, you could implement a more accurate ODE solver or use finer step sizes.