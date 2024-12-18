from cluster import KMeansClustering
from harversian import HaversineCalculator
import pandas as pd

class CityLocator:
    def __init__(self, city_data_file, k=10):
        self.city_data_file = city_data_file
        self.k = k
        self.city_data = None
        self.centroids = []
        self.calculator = HaversineCalculator()

    def load_data(self):
        self.city_data = pd.read_csv(self.city_data_file)

    def cluster_cities(self):
        kmeans = KMeansClustering(self.city_data, self.k)
        self.city_data, self.centroids = kmeans.fit()

    def find_closest_city(self, user_lat, user_lon):
        min_distance = float('inf')
        closest_cluster = None
        for i, (centroid_lat, centroid_lon) in enumerate(self.centroids):
            distance = self.calculator.haversine(user_lat, user_lon, centroid_lat, centroid_lon)
            if distance < min_distance:
                min_distance = distance
                closest_cluster = i

        cities_in_cluster = self.city_data[self.city_data['Cluster'] == closest_cluster]
        closest_city, city_distance = None, float('inf')
        for _, row in cities_in_cluster.iterrows():
            distance = self.calculator.haversine(user_lat, user_lon, row['Latitude'], row['Longitude'])
            if distance < city_distance:
                city_distance = distance
                closest_city = row['City']

        return closest_city, city_distance

    def run(self):
        self.load_data()
        self.cluster_cities()

        try:
            user_lat = float(input("Enter Latitude: "))
            user_lon = float(input("Enter Longitude: "))

            closest_city, city_distance = self.find_closest_city(user_lat, user_lon)
            print(f"\nYou are closest to: {closest_city}")
            print(f"Distance to {closest_city}: {city_distance:.2f} km")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    city_locator = CityLocator('city_data.csv', k=10)
    city_locator.run()
