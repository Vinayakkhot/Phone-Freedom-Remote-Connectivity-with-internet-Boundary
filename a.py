from geopy.geocoders import Nominatim

def get_city_name(lat, long):
    # Initialize the geolocator
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Reverse geocode the coordinates
    location = geolocator.reverse((lat, long), language='en')

    # Extract the city name from the address
    city = location.raw['address']['city']

    return city

# Example usage:
lat = 14.6154  # Example latitude
long = 75.6288 # Example longitude

city_name = get_city_name(lat, long)
print("City:", city_name)

