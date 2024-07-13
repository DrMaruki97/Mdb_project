import pymongo
from geopy.geocoders import Nominatim
from purchase import acquista_biglietti

def get_db():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = pymongo.MongoClient(uri)
    return client["concerti_biglietti"]

def get_coordinates(address):
    geolocator = Nominatim(user_agent="find_coordinates")
    location = geolocator.geocode(address)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

def cerca_concerto(username):
    db = get_db()
    print("Trova i tuoi concerti preferiti tra 254 disponibili:")
    print("a: Per Artista")
    print("b: Per Date")
    print("v: Per Vicinanza")
    scelta = input("> ")

    query = {}
    
    if scelta == 'a':
        artista = input("Artista ?: ")
        artista_doc = db.artisti.find_one({"nome": artista})
        if artista_doc:
            query["artista_id"] = artista_doc["_id"]
        else:
            print("Artista non trovato.")
            return
    elif scelta == 'b':
        data_inizio = input("Data inizio (AAAA-MM-GG): ")
        data_fine = input("Data fine (AAAA-MM-GG): ")
        query["data"] = {"$gte": data_inizio, "$lte": data_fine}
    elif scelta == 'v':
        address = input("Inserisci l'indirizzo: ")
        coordinates = get_coordinates(address)
        if not coordinates:
            print(f"Impossibile ottenere le coordinate per {address}")
            return
        
        lat, lon = coordinates
        distanza = 7  # km
        while True:
            location_docs = db.location.find({
                "coordinate": {
                    "$geoWithin": {
                        "$centerSphere": [[lon, lat], distanza / 6378.1]  # Raggio della Terra in km
                    }
                }
            })
            location_ids = [loc["_id"] for loc in location_docs]
            query["location_id"] = {"$in": location_ids}

            if db.concerti.count_documents(query) > 0:
                break
            else:
                print(f"Nessun concerto trovato entro {distanza} km.")
                scelta = input("Vuoi estendere la distanza di ricerca? (s/n): ")
                if scelta.lower() != 's':
                    return
                try:
                    distanza = int(input("Inserisci una nuova distanza in km per estendere la ricerca: "))
                except ValueError:
                    print("Inserisci un valore numerico.")
                    continue

    concerti = list(db.concerti.find(query))

    if not concerti:
        print("Nessun concerto trovato.")
    else:
        print("Concerti trovati:")
        for idx, concerto in enumerate(concerti):
            location = db.location.find_one({"_id": concerto["location_id"]})
            artista = db.artisti.find_one({"_id": concerto["artista_id"]})
            print(f"{idx+1}: {concerto.get('nome')}, {concerto.get('data')}, disp:{concerto.get('disp', 'N/A')}, {concerto.get('prezzo', 'N/A')}€, Artista: {artista.get('nome', 'N/A')}, Location: {location.get('nome', 'N/A')}")
        
        acquista_subito = input("Vuoi acquistare i biglietti per uno dei concerti trovati? (s/n): ")
        if acquista_subito.lower() == 's':
            acquista_biglietti(username, concerti)