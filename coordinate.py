from geopy.geocoders import Nominatim

def get_coordinates(address):
    # Utilizza un user_agent descrittivo
    geolocator = Nominatim(user_agent="find_coordinates")
    
    # Ottieni la localizzazione dell'indirizzo
    location = geolocator.geocode(address)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Esempio di utilizzo
address = "Piazza del Colosseo, Roma, Italia"
coordinates = get_coordinates(address)

if coordinates:
    print(f"Le coordinate di {address} sono: {coordinates}")
else:
    print(f"Impossibile ottenere le coordinate per {address}")
