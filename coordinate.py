from geopy.geocoders import Nominatim

def get_coordinates(address):
    geolocator = Nominatim(user_agent="find_coordinates")

    location = geolocator.geocode(address)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

address = "Bellinzago Lombardo"
coordinates = get_coordinates(address)

if coordinates:
    print(f"Le coordinate di {address} sono: {coordinates}")
else:
    print(f"Impossibile ottenere le coordinate per {address}")
