import json
from pymongo import MongoClient
import os

def carica_dati():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = MongoClient(uri)
    db = client["concerti_biglietti"]

    # Rimuovere eventuali dati esistenti
    db.artisti.drop()
    db.concerti.drop()
    db.location.drop()

    base_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(base_path, "../data")

    # Caricare dati artisti
    with open(os.path.join(data_path, "artisti.json")) as f:
        artisti = json.load(f)
        try:
            db.artisti.insert_many(artisti, ordered=False)
        except Exception as e:
            print(f"Errore durante l'inserimento degli artisti: {e}")

    # Caricare dati concerti
    with open(os.path.join(data_path, "concerti.json")) as f:
        concerti = json.load(f)
        try:
            db.concerti.insert_many(concerti, ordered=False)
        except Exception as e:
            print(f"Errore durante l'inserimento dei concerti: {e}")

    # Caricare dati location
    with open(os.path.join(data_path, "location.json")) as f:
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
