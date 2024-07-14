import pymongo
from geopy.geocoders import Nominatim
from purchase import acquista_biglietti
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.style import Style

console = Console()

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
    console.print(Panel("Trova i tuoi concerti preferiti tra 254 disponibili:\na: Per Artista\nb: Per Date\nc: Per Nome\nv: Per Vicinanza", title="Cerca Concerto", style="cyan"))
    scelta = input("> ")

    query = {}
    
    if scelta == 'a':
        artista = input("Artista ?: ")
        artisti_docs = db.artisti.find({"nome": {"$regex": artista, "$options": "i"}})
        artisti_ids = [artista_doc["_id"] for artista_doc in artisti_docs]
        
        if not artisti_ids:
            console.print("[red]Nessun artista trovato.[/red]")
            return

        query["artista_id"] = {"$in": artisti_ids}
        
    elif scelta == 'b':
        data_inizio = input("Data inizio (AAAA-MM-GG): ")
        data_fine = input("Data fine (AAAA-MM-GG): ")
        query["data"] = {"$gte": data_inizio, "$lte": data_fine}
    
    elif scelta == 'c':
        nome_concerto = input("Nome del concerto ?: ")
        query["nome"] = {"$regex": nome_concerto, "$options": "i"}
    
    elif scelta == 'v':
        address = input("Inserisci l'indirizzo: ")
        coordinates = get_coordinates(address)
        if not coordinates:
            console.print(f"[red]Impossibile ottenere le coordinate per {address}[/red]")
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
                console.print(f"[red]Nessun concerto trovato entro {distanza} km.[/red]")
                scelta = input("Vuoi estendere la distanza di ricerca? (s/n): ")
                if scelta.lower() != 's':
                    return
                try:
                    distanza = int(input("Inserisci una nuova distanza in km per estendere la ricerca: "))
                except ValueError:
                    console.print("[red]Inserisci un valore numerico.[/red]")
                    continue

    concerti = list(db.concerti.find(query))

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
            location = db.location.find_one({"_id": concerto["location_id"]})
            artista = db.artisti.find_one({"_id": concerto["artista_id"]})
            settori = concerto.get('settori', [])
            
            prezzi_disponibili = [settore['prezzo'] for settore in settori if settore['posti_disponibili'] > 0]
            prezzo_min = min(prezzi_disponibili) if prezzi_disponibili else 'Sold Out'
            disponibilita = 'Disponibile' if prezzi_disponibili else 'Sold Out'
            
            location_nome = location.get('nome', 'N/A') if location else 'N/A'
            artista_nome = artista.get('nome', 'N/A') if artista else 'N/A'

            if disponibilita == 'Sold Out':
                table.add_row(str(idx + 1), concerto.get('nome'), concerto.get('data'), disponibilita, prezzo_min, artista_nome, location_nome, style=sold_out_style)
            else:
                table.add_row(str(idx + 1), concerto.get('nome'), concerto.get('data'), disponibilita, f"{prezzo_min}€", artista_nome, location_nome)
        
        console.print(table)

        acquista_subito = input("Vuoi acquistare i biglietti per uno dei concerti trovati? (s/n): ")
        while acquista_subito.lower() not in ('s', 'n'):
            console.print("[red]Scelta non valida, riprova.[/red]")
            acquista_subito = input("Vuoi acquistare i biglietti per uno dei concerti trovati? (s/n): ")
        if acquista_subito.lower() == 's':
            acquista_biglietti(username, concerti)
