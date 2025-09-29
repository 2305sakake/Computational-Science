import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from scipy.stats import multivariate_normal

# Parameters
n = 300      # Number of points in each dataset
k = 2        # Number of clusters
max_it = 100 # Maximum number of iterations

# Initialize 4 groups of data points
datasets = []
for i in range(4):
    dataset, _ = make_classification(
        n_samples=n,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        n_clusters_per_class=1,
        n_classes=k,
        random_state=i
    )
    datasets.append(dataset)

def log_likelihood(points, means, covs, weights, k):
    """Calculates log likelihood function"""
    pdfs = np.array([weights[i] * multivariate_normal.pdf(points, means[i], covs[i]) for i in range(k)]).T
    return np.sum(np.log(pdfs.sum(axis=1)))

def initialize_params(points, k):
    """Initializes means, covariances, and weights for each Gaussian"""
    means = points[np.random.choice(points.shape[0], k, replace=False)]
    covs = [np.eye(2) for _ in range(k)]
    weights = np.full(k, 1/k)
    return means, covs, weights

def expectation_step(points, means, covs, weights, k):
    """Performs expectation step in EM algorithm and returns responsibilities array"""
    num = np.empty((len(points), k))
    for i in range(k):
        num[:, i] = weights[i] * multivariate_normal.pdf(points, means[i], covs[i])
    return num / num.sum(axis=1, keepdims=True)

def maximization_step(points, means, covs, weights, responsibilities, k, n):
    """Peforms maximization step in EM algorithm and returns updated parameters"""
    Ns = responsibilities.sum(axis=0)

    new_means = np.empty_like(means)
    new_covs  = np.empty_like(covs)
    new_weights = np.empty_like(weights)

    # Update parameters using caclulated responsibilities
    for i in range(k):
        N_i = Ns[i]
        responsibility = responsibilities[:,i]

        new_means[i] = (responsibility[:, np.newaxis] * points).sum(axis=0) / N_i

        difference = points - new_means[i]
        new_covs[i] = (difference.T * responsibility) @ difference / N_i + 1e-6 * np.eye(2)

        new_weights[i] = N_i / n

    return new_means, new_covs, new_weights

def gmm_algorithm(points, k, max_it):
    """Performs Gaussian mixture model algorithm until convergence in the log likelihood function is reached"""
    means, covs, weights = initialize_params(points, k)
    ll = None # Value for log likelihood funciton

    for _ in range(max_it):
        responsibilities = expectation_step(points, means, covs, weights, k)
        means, covs, weights = maximization_step(points, means, covs, weights, responsibilities, k, n)
        new_ll = log_likelihood(points, means, covs, weights, k)

        # Check for convergence
        if ll is not None and abs(ll - new_ll) < 1e-4:
            break 
        ll = new_ll
    
    responsibilities = expectation_step(points, means, covs, weights, k)
    labels = np.argmax(responsibilities, axis=1)

    return labels

fig, axes = plt.subplots(2, 2, figsize=(9, 9))
fig.suptitle("Gaussian Mixture Model Algorithm on 4 Different Datasets")

# Perform algorithm on the different datasets and plot
for ax, dataset in zip(axes.flat, datasets):
    labels = gmm_algorithm(dataset, k, max_it)

    for label in range(k):
        points = dataset[labels == label]
        ax.scatter(points[:, 0], points[:, 1], s=10)

plt.tight_layout()
plt.show()
