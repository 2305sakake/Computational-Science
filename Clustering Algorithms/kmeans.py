import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification

# Parameters
n = 300      # Number of points in each dataset
k = 2        # Number of clusters
max_it = 50  # Maximum number of iterations

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

def initialize_centroids(points, k):
    """Randomly choose centroids from data points"""
    indices = np.random.choice(points.shape[0], k, replace=False)
    return points[indices]

def label_points(points, centroids):
    """Assign each point to its closest centroid"""
    distances = np.linalg.norm(points[:, np.newaxis] - centroids, axis=2)
    return np.argmin(distances, axis=1)

def update_centroids(points, labels, k):
    """Recompute new centroids as the mean of each group of assigned points"""
    return np.array([points[labels == i].mean(axis=0) for i in range(k)])

def k_means(points, k, max_it):
    """Performs k-means algorithm"""
    current_centroids = initialize_centroids(points, k)

    for _ in range(max_it):
        labels = label_points(points, current_centroids)
        new_centroids = update_centroids(points, labels, k)

        if np.linalg.norm(new_centroids - current_centroids) < 1e-4:
            break

        current_centroids = new_centroids
    return labels

# Perform algorithm on the different datasets and plot
fig, axes = plt.subplots(2, 2, figsize=(9, 9))
fig.suptitle("K-Means Algorithm on 4 Different Datasets")

for ax, dataset in zip(axes.flat, datasets):
    labels = k_means(dataset, k, max_it)

    for label in range(k):
        points = dataset[labels == label]
        ax.scatter(points[:, 0], points[:, 1], s=10)

plt.tight_layout()
plt.show()
