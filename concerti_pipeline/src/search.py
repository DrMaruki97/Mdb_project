import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from geopy.geocoders import Nominatim
from purchase import acquista_biglietti
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.style import Style
from auth import get_db

console = Console()

def get_coordinates(address):
    geolocator = Nominatim(user_agent="find_coordinates")
    location = geolocator.geocode(address)
    
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

def cerca_concerto(username):
    db = get_db()
    console.print(Panel("Trova i tuoi concerti preferiti tra quelli disponibili:\na: Per Artista\nb: Per Date\nc: Per Nome\nv: Per Vicinanza", title="Cerca Concerto", style="cyan"))
    scelta = input("> ")

    pipeline = []
    
    if scelta == 'a':
        artista = input("Artista?: ")
        pipeline.extend([
            {"$lookup": {
                "from": "artisti",
                "localField": "artista_id",
                "foreignField": "_id",
                "as": "artista"
            }},
            {"$match": {"artista.nome": {"$regex": artista, "$options": "i"}}},
            {"$unwind": "$artista"}
        ])
        
    elif scelta == 'b':
        data_inizio = input("Data inizio (AAAA-MM-GG): ")
        data_fine = input("Data fine (AAAA-MM-GG): ")
        pipeline.append({"$match": {"data": {"$gte": data_inizio, "$lte": data_fine}}})
    
    elif scelta == 'c':
        nome_concerto = input("Nome del concerto ?: ")
        pipeline.append({"$match": {"nome": {"$regex": nome_concerto, "$options": "i"}}})
    
    elif scelta == 'v':
        address = input("Inserisci l'indirizzo: ")
        coordinates = get_coordinates(address)
        if not coordinates:
            console.print(f"[red]Impossibile ottenere le coordinate per {address}[/red]")
            return
        
        lat, lon = coordinates
        distanza = 7  # km
        while True:
            location_docs = list(db.location.aggregate([
                {"$geoNear": {
                    "near": {"type": "Point", "coordinates": [lon, lat]},
                    "distanceField": "distanza",
                    "maxDistance": distanza * 1000,
                    "spherical": True
                }},
                {"$project": {"_id": 1}}
            ]))
            location_ids = [loc["_id"] for loc in location_docs]
            pipeline.append({"$match": {"location_id": {"$in": location_ids}}})

            if db.concerti.count_documents({"$and": pipeline}) > 0:
                break
            else:
                console.print(f"[red]Nessun concerto trovato entro {distanza} km.[/red]")
                scelta = input("Vuoi estendere la distanza di ricerca? (s/n): ")
                if scelta.lower() != 's':
                    return
                try:
                    distanza = int(input("Inserisci una nuova distanza in km per estendere la ricerca: "))
                except ValueError:
                    console.print("[red]Inserisci un valore numerico.[/red]")
                    continue

    pipeline.extend([
        {"$lookup": {
            "from": "artisti",
            "localField": "artista_id",
            "foreignField": "_id",
            "as": "artista"
        }},
        {"$lookup": {
            "from": "location",
            "localField": "location_id",
            "foreignField": "_id",
            "as": "location"
        }},
        {"$unwind": "$artista"},
        {"$unwind": "$location"},
        {"$project": {
            "nome": 1,
            "data": 1,
            "settori": 1,
            "artista_nome": "$artista.nome",
            "location_nome": "$location.nome"
        }}
    ])

    concerti = list(db.concerti.aggregate(pipeline))

    if not concerti:
        console.print("[red]Nessun concerto trovato.[/red]")
    else:
        table = Table(title="Concerti trovati")
        table.add_column("Index", justify="right", style="cyan", no_wrap=True)
        table.add_column("Concerto", style="magenta")
        table.add_column("Data", style="green")
        table.add_column("Disponibilità", style="red")
        table.add_column("Prezzi a partire da", style="yellow")
        table.add_column("Artista", style="blue")
        table.add_column("Location", style="blue")

        sold_out_style = Style(color="red", strike=True)

        for idx, concerto in enumerate(concerti):
            settori = concerto.get('settori', [])
            prezzi_disponibili = [settore['prezzo'] for settore in settori if settore['posti_disponibili'] > 0]
            prezzo_min = min(prezzi_disponibili) if prezzi_disponibili else 'Sold Out'
            disponibilita = 'Disponibile' if prezzi_disponibili else 'Sold Out'

            if disponibilita == 'Sold Out':
                table.add_row(str(idx + 1), concerto.get('nome'), concerto.get('data'), disponibilita, prezzo_min, concerto['artista_nome'], concerto['location_nome'], style=sold_out_style)
            else:
                table.add_row(str(idx + 1), concerto.get('nome'), concerto.get('data'), disponibilita, f"{prezzo_min}€", concerto['artista_nome'], concerto['location_nome'])
        
        console.print(table)

        acquista_subito = input("Vuoi acquistare i biglietti per uno dei concerti trovati? (s/n): ")
        while acquista_subito.lower() not in ('s', 'n'):
            console.print("[red]Scelta non valida, riprova.[/red]")
            acquista_subito = input("Vuoi acquistare i biglietti per uno dei concerti trovati? (s/n): ")
        if acquista_subito.lower() == 's':
            acquista_biglietti(username, concerti)
