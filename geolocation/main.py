from cluster import KMeansClustering
from harversian import HaversineCalculator
import pandas as pd
from location import Location
from direction import Direction

class CityLocator:
    def __init__(self, city_data_file, k=10):
        self.city_data_file = city_data_file
        self.k = k
        self.city_data = None
        self.centroids = []
        self.calculator = HaversineCalculator()
        self.location = Location()
        self.direction = Direction()


    def load_data(self):
        city_raw_data = pd.read_csv(self.city_data_file)
        city_raw_data['City'] = city_raw_data['City'].str.lower()
        self.city_data = city_raw_data

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
    def find_distance_to_city(self, user_lat, user_lon, city_name):
        city_row = self.city_data[self.city_data['City'].str.lower() == city_name.lower()]
        
        if city_row.empty:
            return None, None 
        
        city_lat = city_row.iloc[0]['Latitude']
        city_lon = city_row.iloc[0]['Longitude']
        distance = self.calculator.haversine(user_lat, user_lon, city_lat, city_lon)
        bearing = self.direction.calculate_bearing(user_lat, user_lon, city_lat, city_lon)
        direct = self.direction.get_compass_direction(bearing)
        
        return city_name, distance, direct

    def run(self):
        self.load_data()
        self.cluster_cities()

        try:
            print("Choose the option")
            print("Option 1: Find the city based on lat and long")
            print("Option 2: Calculate distance of any city from your location")
            choice = int(input("Enter the choice: "))

            if choice == 1:
                user_lat = float(input("Enter Latitude: "))
                user_lon = float(input("Enter Longitude: "))

                closest_city, city_distance = self.find_closest_city(user_lat, user_lon)
                print(f"\nYou are closest to: {closest_city}")
                print(f"Distance to {closest_city}: {city_distance:.2f} km")
            elif choice == 2:
                city_name = input("Enter the city name: ")
                latitude, longitude = self.location.getLocation()
                city_name, distance, direct = self.find_distance_to_city(latitude, longitude, city_name)

                if city_name:
                    print(f"Distance to {city_name} is {distance} K M in {direct}")

        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    city_locator = CityLocator('city_data.csv', k=10)
    city_locator.run()
