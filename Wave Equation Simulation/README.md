# Wave Equation Simulation

## Overview

In this project, I have created two programs that simulate the motion of a wave in one dimensions and two dimensions by solving the wave equation with Dirichlet boundary conditions using a finite difference approximation. The motion of the wave is then visualized on matplotlib. Details of the program are given below.

## Details

### One Dimensional Wave Simulation

As explained above, 1D_wave.py simulates the solution to the one dimensional wave equation using a finite difference approach. A few things to be noted about the code are as follows. 

First of all, when defining the necessary parameters, we allow dx to be freely chosen by the user but not dt. This is because due to the Courant-Friedrichs-Lewy condition, we require that the Courant number, c*dt/dx, is less than or equal to 1 for numerical stability. To ensure this, we choose the Courant number to be 0.99 and calculate dt from there. 

Another thing that should be noted is that since the finite difference approximation requires information from *two* previous time steps (despite us only having our one initial state), we also calculate the displacements in the second time step under the assumption that the string is initially at rest. This is done immediately after defining the initial state as indicated in the program.

Otherwise, the program is quite self-explanatory and you can feel free to play around with different intial conditions. 

### Two Dimensional Wave Simulation

Generalizing the previous code to two dimensions is quite straightforward and we only need to make a few changes with the way we plot the wave and our finite difference approximation. One thing that should be noted however is that we can no longer use 0.99 as our Courant number since the CFL condition in the 2D case now requires that it is less than the square root of 2 instead. This is accounted for by setting C to 0.7. As with before, you can feel free to test different initial conditions.

A sample run of the program is shown below:
![Sample run of 2D_wave.py](2D_wave.gif)

