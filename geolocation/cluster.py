import random
import pandas as pd
from harversian import harvesian



def select_centroids(city_data, k):
    centroids = random.sample(list(city_data[['Latitude', 'Longitude']].values), k)
    return centroids


def assign_clusters(city_data, centroids):
    clusters = []
    for _, row in city_data.iterrows():
        min_distance = float('inf')
        closest_centroid = None
        for i, (centroid_lat, centroid_lon) in enumerate(centroids):
            distance = harvesian(row['Latitude'], row['Longitude'], centroid_lat, centroid_lon)
            if distance < min_distance:
                min_distance = distance
                closest_centroid = i
        clusters.append(closest_centroid)
    return clusters

def update_centroids(city_data, clusters, k):
    new_centroids = []
    for cluster in range(k):
        cluster_points = city_data[clusters == cluster]
        if not cluster_points.empty:
            avg_lat = cluster_points['Latitude'].mean()
            avg_lon = cluster_points['Longitude'].mean()
            new_centroids.append((avg_lat, avg_lon))
        else:
            new_centroids.append(random.choice(list(city_data[['Latitude', 'Longitude']].values)))
    return new_centroids

def k_means_clustering(city_data, k, max_iterations=100, tolerance=1e-4):
    centroids = select_centroids(city_data, k)
    
    for _ in range(max_iterations):
        clusters = assign_clusters(city_data, centroids)
        city_data['Cluster'] = clusters
        
        new_centroids = update_centroids(city_data, city_data['Cluster'], k)
        
        shifts = [harvesian(c1[0], c1[1], c2[0], c2[1]) for c1, c2 in zip(centroids, new_centroids)]
        if max(shifts) < tolerance:
            break
        centroids = new_centroids
    
    return city_data, centroids