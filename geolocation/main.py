from cluster import k_means_clustering
from harversian import harvesian
import pandas as pd

def main():
    csv_data = 'city_data.csv'
    city_data = pd.read_csv(csv_data)
    
    k = 10
    city_data, centroids = k_means_clustering(city_data, k)
    
    try:
        user_lat = float(input("Enter Latitude: "))
        user_lon = float(input("Enter Longitude: "))

        min_distance = float('inf')
        closest_cluster = None
        for i, (centroid_lat, centroid_lon) in enumerate(centroids):
            distance = harvesian(user_lat, user_lon, centroid_lat, centroid_lon)
            if distance < min_distance:
                min_distance = distance
                closest_cluster = i

        cities_in_cluster = city_data[city_data['Cluster'] == closest_cluster]
        closest_city, city_distance = None, float('inf')
        for _, row in cities_in_cluster.iterrows():
            distance = harvesian(user_lat, user_lon, row['Latitude'], row['Longitude'])
            if distance < city_distance:
                city_distance = distance
                closest_city = row['City']

        print(f"\nYou are closest to: {closest_city}")
        print(f"Distance to {closest_city}: {city_distance:.2f} km")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
