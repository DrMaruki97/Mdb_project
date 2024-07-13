import pymongo
from utils import get_db

def crea_concerto(username):
    db = get_db()
    
    nome_concerto = input("Nome del concerto: ")
    data = input("Data del concerto (AAAA-MM-GG): ")
    location_nome = input("Nome della location: ")
    coordinate = input("Coordinate della location (lat, lon): ").split(",")
    indirizzo = input("Indirizzo della location: ")
    location_id = f"{location_nome.replace(' ', '_')}_{coordinate[0]}_{coordinate[1]}"
    
    location = {
        "_id": location_id,
        "nome": location_nome,
        "coordinate": {
            "type": "Point",
            "coordinates": [float(coordinate[1]), float(coordinate[0])]
        },
        "indirizzo": indirizzo
    }
    
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
    
    db.location.update_one({"_id": location_id}, {"$set": location}, upsert=True)
    db.concerti.insert_one(concerto)
    print("Concerto creato con successo!")

def visualizza_situazione_biglietti(username):
    db = get_db()
    concerti = db.concerti.find({"artista_id": username})
    
    for concerto in concerti:
        print(f"Concerto: {concerto['nome']}, Data: {concerto['data']}")
        for settore in concerto['settori']:
            print(f"    Settore: {settore['nome']}, Posti rimanenti: {settore['posti_disponibili']}")
            
def duplica_concerto(username):
    db = get_db()
    concerti = list(db.concerti.find({"artista_id": username}))
    
    for idx, concerto in enumerate(concerti):
        print(f"{idx+1}: {concerto['nome']}, {concerto['data']}")
        
    scelta = int(input("Quale concerto vuoi duplicare? ")) - 1
    nuova_data = input("Inserisci la nuova data (AAAA-MM-GG): ")
    
    concerto_da_duplicare = concerti[scelta]
    nuovo_concerto = concerto_da_duplicare.copy()
    nuovo_concerto['_id'] = None
    nuovo_concerto['data'] = nuova_data
    
    db.concerti.insert_one(nuovo_concerto)
    print("Concerto duplicato con successo!")

def visualizza_utenti_biglietti(username):
    db = get_db()
    concerti = db.concerti.find({"artista_id": username})
    
    for concerto in concerti:
        print(f"Concerto: {concerto['nome']}, Data: {concerto['data']}")
        utenti = db.utenti.find({"biglietti.concerti_id": concerto['_id']})
        for utente in utenti:
            biglietti_utente = [biglietto for biglietto in utente['biglietti'] if biglietto['concerto'] == concerto['nome']]
            for biglietto in biglietti_utente:
                print(f"    Utente: {utente['username']}, Settore: {biglietto['settore']}, Quantità: {biglietto['quantita']}")
