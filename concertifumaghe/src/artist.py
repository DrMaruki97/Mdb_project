import pymongo
from geopy.geocoders import Nominatim
from utils import get_db

def crea_concerto(username):
    db = get_db()
    geolocator = Nominatim(user_agent="concert_creator")

    nome_concerto = input("Nome del concerto: ")
    data = input("Data del concerto (AAAA-MM-GG): ")
    location_nome = input("Nome della location: ")

    location = db.location.find_one({"nome": location_nome})
    
    if location:
        location_id = location["_id"]
    else:
        location_geocode = geolocator.geocode(location_nome)
        if not location_geocode:
            print(f"Impossibile trovare le coordinate per {location_nome}")
            return
        
        location_id = f"{location_nome.replace(' ', '_')}_{location_geocode.latitude}_{location_geocode.longitude}"
        location_doc = {
            "_id": location_id,
            "nome": location_nome,
            "coordinate": {
                "type": "Point",
                "coordinates": [location_geocode.longitude, location_geocode.latitude]
            },
            "indirizzo": location_geocode.address
        }
        db.location.insert_one(location_doc)

    settori = []
    n_settori = int(input("Numero di settori: "))
    for _ in range(n_settori):
        settore_nome = input("Nome del settore: ")
        prezzo = float(input("Prezzo del settore: "))
        posti_disponibili = int(input("Posti disponibili: "))
        settori.append({
            "nome": settore_nome,
            "prezzo": prezzo,
            "posti_disponibili": posti_disponibili
        })

    concerto = {
        "nome": nome_concerto,
        "data": data,
        "artista_id": username,
        "location_id": location_id,
        "settori": settori
    }

    db.concerti.insert_one(concerto)
    print("Concerto creato con successo!")

def visualizza_situazione_biglietti(username):
    db = get_db()
    concerti = list(db.concerti.find({"artista_id": username}))
    
    if len(concerti) == 0:
        print("Nessun concerto trovato per l'artista.")
        return
    
    for concerto in concerti:
        print(f"Concerto: {concerto['nome']}, Data: {concerto['data']}")
        for settore in concerto['settori']:
            print(f"    Settore: {settore['nome']}, Posti rimanenti: {settore['posti_disponibili']}")
            
def duplica_concerto(username):
    db = get_db()
    concerti = list(db.concerti.find({"artista_id": username}))
    
    if not concerti:
        print("Nessun concerto trovato per l'artista.")
        return
    
    for idx, concerto in enumerate(concerti):
        print(f"{idx+1}: {concerto['nome']}, {concerto['data']}")
        
    try:
        scelta = int(input("Quale concerto vuoi duplicare? ")) - 1
        if scelta < 0 or scelta >= len(concerti):
            print("Scelta non valida.")
            return
    except ValueError:
        print("Inserisci un valore numerico valido.")
        return

    nuova_data = input("Inserisci la nuova data (AAAA-MM-GG): ")
    
    concerto_da_duplicare = concerti[scelta]
    nuovo_concerto = concerto_da_duplicare.copy()
    nuovo_concerto['_id'] = None
    nuovo_concerto['data'] = nuova_data
    
    db.concerti.insert_one(nuovo_concerto)
    print("Concerto duplicato con successo!")

def visualizza_utenti_biglietti(username):
    db = get_db()
    concerti = list(db.concerti.find({"artista_id": username}))
    
    if len(concerti) == 0:
        print("Nessun concerto trovato per l'artista.")
        return
    
    for concerto in concerti:
        print(f"Concerto: {concerto['nome']}, Data: {concerto['data']}")
        utenti = list(db.utenti.find({"biglietti.concerti_id": concerto['_id']}))
        if len(utenti) == 0:
            print("Nessun utente ha acquistato i biglietti per questo concerto.")
            continue
        for utente in utenti:
            biglietti_utente = [biglietto for biglietto in utente['biglietti'] if biglietto['concerto'] == concerto['nome']]
            for biglietto in biglietti_utente:
                print(f"    Utente: {utente['username']}, Settore: {biglietto['settore']}, Quantità: {biglietto['quantita']}")
