import numpy as np
from sklearn.cluster import KMeans, MeanShift

def big_crunch_meanshift(population, fitnesses, bandwidth=1.0):
    X = np.array(population, dtype=float)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=False)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    centers = []
    for i in range(len(cluster_centers)):
        members = [j for j, label in enumerate(labels) if label == i]
        if members:
            best = min(members, key=lambda idx: fitnesses[idx])
            centers.append(population[best])
    return centers

def big_crunch_kmeans(population, fitnesses, n_clusters=5):
    X = np.array(population, dtype=float)
    kmeans = KMeans(n_clusters=min(n_clusters, len(population)), n_init='auto', random_state=42)
    labels = kmeans.fit_predict(X)
    centers = []
    for i in range(kmeans.n_clusters):
        members = [j for j, label in enumerate(labels) if label == i]
        if members:
            best = min(members, key=lambda idx: fitnesses[idx])
            centers.append(population[best])
    return centers
