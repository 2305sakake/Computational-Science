# Eigenfaces

## Overview
`eigenfaces.ipynb` includes a program that takes a set of images from the Extended Yale Face Database B and performs principal component analysis (PCA) on them to find the eigenvectors or 'eigenfaces' as we will be calling them. To perform the PCA, we use NumPy's built in singular value decomposition (SVD) function on the mean-subtracted data and the eigenfaces can be extracted from the computed V vector. We can also use the eigenfaces that we have calculated and only use the most significant ones and recreate images that were not in the data. Much of this is inspired from Brunton and Kutz's "Data-Driven Science and Engineering Machine Learning, Dynamical Systems, and Control".

Further details and sample plots of images can be found in the Jupyter notebook.
