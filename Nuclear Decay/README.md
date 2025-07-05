# Nuclear Decay Simulation

## Overview

This is a program that I made on MATLAB that visually simulates the nuclear decay of a large number of particles. The basic setup is that we have an n x n grid of an element X, each with some probability to decay into another element, Y, represented by a different color. This second element Y also has some probability to decay into a further element, Z. As time goes by, we see the pixels in the grid slowly changing color as each element decays.

## Details

This program works by making of use of logical arrays to represent whether the corresponding pixel is X, Y, or Z. Each of the three elements have their corresponding logical array where 1 means that this pixel is this element and 0 means it is not (this means the sum of all three logical arrays should be an array with all ones). Then, we create a function called currentpop which updates the population by determining whether each element has decayed or not. The probability of decay is calculated from the halflife of X and Y inputted from the user. For a given population, a visual representation can be created by scaling each array differently, adding them together, and then using the image function. This whole process is then iterated over a certain number of years and finally converted into an animation.