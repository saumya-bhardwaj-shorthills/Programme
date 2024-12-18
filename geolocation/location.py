import geocoder

class Location:
    def __init__(self):
        pass

    def getLocation(self):
        g = geocoder.ip('me')  # Fetch location using IP
        if g.ok:
            print(g.latlng)
            return g.latlng  # Returns [latitude, longitude]
        else:
            print("Error")
            return None
        
