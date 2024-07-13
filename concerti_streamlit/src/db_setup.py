import json
from pymongo import MongoClient

def carica_dati():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = MongoClient(uri)
    db = client["concerti_biglietti"]

    # Rimuovere eventuali dati esistenti
    db.artisti.drop()
    db.concerti.drop()
    db.location.drop()

    # Caricare dati artisti
    with open("data/artisti.json") as f:
        artisti = json.load(f)
        try:
            db.artisti.insert_many(artisti, ordered=False)
        except Exception as e:
            print(f"Errore durante l'inserimento degli artisti: {e}")

    # Caricare dati concerti
    with open("data/concerti.json") as f:
        concerti = json.load(f)
        try:
            db.concerti.insert_many(concerti, ordered=False)
        except Exception as e:
            print(f"Errore durante l'inserimento dei concerti: {e}")

    # Caricare dati location
    with open("data/location.json") as f:
        location = json.load(f)
        try:
            db.location.insert_many(location, ordered=False)
        except Exception as e:
            print(f"Errore durante l'inserimento delle location: {e}")

    # Creazione indice geospaziale
    db.location.create_index([("coordinate", "2dsphere")])

    print("Dati caricati con successo e indice geospaziale creato!")

if __name__ == "__main__":
    carica_dati()
