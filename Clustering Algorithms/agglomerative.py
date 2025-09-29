import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from sklearn.datasets import make_classification
import heapq

# Parameters
n = 300  # Number of points in each dataset
k = 2    # Number of clusters

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

def agglomerative(points, k, n):
    # Initialize heap of each pairwise Ward distance
    heap = [(0.5 * np.sum((points[i] - points[j]) ** 2), i, j) for i, j in combinations(range(n), 2)]
    heapq.heapify(heap)

    # Initialize cluster dictionary
    clusters = {i: {i} for i in range(n)}

    # Set up variable for new keys for the clusters dictionary
    new_idx = n + 1

    while len(clusters) > k:
        # Extract closest pair from heap
        _, i, j = heapq.heappop(heap)

        if i not in clusters or j not in clusters:
            continue

        # Merge and delete clusters from clusters dictionary
        new_cluster = clusters[i] | clusters[j]
        del clusters[i], clusters[j]

        # Calculate centroid and size of new cluster
        new_centroid = points[list(new_cluster)].mean(axis=0)
        new_size = len(new_cluster)

        # Add ward distances of the new cluster with the other existing clusters
        for other_idx, other_cluster in clusters.items():
            # Compute centroid and size of other cluster
            other_centroid = points[list(other_cluster)].mean(axis=0)
            other_size = len(other_cluster)

            # Calculate ward distance and add to heap
            d = (new_size * other_size) / (new_size + other_size) * np.sum((new_centroid - other_centroid) ** 2)
            heapq.heappush(heap, (d, new_idx, other_idx))

        # Add new cluster to dictionary with its corresponding key 
        clusters[new_idx] = new_cluster
        new_idx += 1
    return list(clusters.values())

# Perform algorithm on the different datasets and plot
fig, axes = plt.subplots(2, 2, figsize=(9, 9))
fig.suptitle("Agglomerative Algorithm with Ward Linkage on 4 Different Datasets")

for ax, dataset in zip(axes.flat, datasets):
    clusters = agglomerative(dataset, k, n)

    for cluster in clusters:
     points = dataset[list(cluster)]
     ax.scatter(points[:, 0], points[:, 1], s=10)

plt.tight_layout()
plt.show()
