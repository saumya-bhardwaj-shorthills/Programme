import math

class Direction:
    def __init__(self):
        pass

    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1

        x = math.sin(dlon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
        initial_bearing = math.atan2(x, y)
        bearing_degrees = (math.degrees(initial_bearing) + 360) % 360
        return bearing_degrees
    
    def get_compass_direction(self, bearing):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = int((bearing + 22.5) % 360 / 45)
        return directions[index]