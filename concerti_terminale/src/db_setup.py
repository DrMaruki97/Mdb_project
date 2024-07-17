import json
from pymongo import MongoClient
import os
from rich.console import Console
from rich.panel import Panel 

console = Console()

def carica_dati():
    uri = "mongodb+srv://lucagiovagnoli:t7g%5EFyi7zpN!Liw@ufs13.dsmvdrx.mongodb.net/"
    client = MongoClient(uri)
    db = client["concerti_biglietti"]

    db.artisti.drop()
    db.concerti.drop()
    db.location.drop()

    base_path = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(base_path, "../data")

    with open(os.path.join(data_path, "artisti.json")) as f:
        artisti = json.load(f)
        try:
            db.artisti.insert_many(artisti, ordered=False)
        except Exception as e:
            console.print(f"[red]Errore durante l'inserimento degli artisti: {e}[/red]")

    with open(os.path.join(data_path, "concerti.json")) as f:
        concerti = json.load(f)
        try:
            db.concerti.insert_many(concerti, ordered=False)
        except Exception as e:
            console.print(f"[red]Errore durante l'inserimento dei concerti: {e}[/red]")

    with open(os.path.join(data_path, "location.json")) as f:
        location = json.load(f)
        try:
            db.location.insert_many(location, ordered=False)
        except Exception as e:
            console.print(f"[red]Errore durante l'inserimento delle location: {e}[/red]")

    db.location.create_index([("coordinate", "2dsphere")])

    console.print("[green]Dati caricati con successo e indice geospaziale creato![/green]")

if __name__ == "__main__":
    carica_dati()
