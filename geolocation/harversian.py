import math


class HaversineCalculator:
    def __init__(self, radius=6371):
        self.radius = radius

    def haversine(self,lat1, long1, lat2, long2):
        lat1 = math.radians(lat1)
        long1 = math.radians(long1)
        lat2 = math.radians(lat2)
        long2 = math.radians(long2)
        lat_angle = (lat1-lat2)/2
        long_angle = (long1-long2)/2
        Y_term = (math.sin(lat_angle))**2
        K_term = (math.sin(long_angle))**2
        Z_term = (math.cos(lat1))*(math.cos(lat2))
        X_term = math.sqrt(Y_term + Z_term*K_term)
        distance = 2* self.radius * X_term
        return distance

if __name__ == "__main__":
    lat1 = 51.5007
    lon1 = 0.1246
    lat2 = 40.6892
    lon2 = 74.0445

    calculator = HaversineCalculator()

    distance = calculator.haversine(lat1,lon1,lat2,lon2)

    print(f"Distance ${distance}")