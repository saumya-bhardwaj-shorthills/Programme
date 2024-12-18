import random
import pandas as pd
from harversian import HaversineCalculator

class KMeansClustering:
    def __init__(self, city_data, k, max_iterations=100, tolerance=1e-4):
        self.city_data = city_data
        self.k = k
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.centroids = []
        self.calculator = HaversineCalculator()

    def initialize_centroids(self):
        self.centroids = random.sample(list(self.city_data[['Latitude', 'Longitude']].values), self.k)

    def assign_clusters(self):
        clusters = []
        for _, row in self.city_data.iterrows():
            min_distance = float('inf')
            closest_centroid = None
            for i, (centroid_lat, centroid_lon) in enumerate(self.centroids):
                distance = self.calculator.haversine(row['Latitude'], row['Longitude'], centroid_lat, centroid_lon)
                if distance < min_distance:
                    min_distance = distance
                    closest_centroid = i
            clusters.append(closest_centroid)
        self.city_data['Cluster'] = clusters

    def update_centroids(self):
        new_centroids = []
        for cluster in range(self.k):
            cluster_points = self.city_data[self.city_data['Cluster'] == cluster]
            if not cluster_points.empty:
                avg_lat = cluster_points['Latitude'].mean()
                avg_lon = cluster_points['Longitude'].mean()
                new_centroids.append((avg_lat, avg_lon))
            else:
                new_centroids.append(random.choice(list(self.city_data[['Latitude', 'Longitude']].values)))
        return new_centroids

    def fit(self):
        self.initialize_centroids()
        for _ in range(self.max_iterations):
            self.assign_clusters()
            new_centroids = self.update_centroids()

            shifts = [self.calculator.haversine(c1[0], c1[1], c2[0], c2[1]) for c1, c2 in zip(self.centroids, new_centroids)]
            if max(shifts) < self.tolerance:
                break
            self.centroids = new_centroids

        return self.city_data, self.centroids
