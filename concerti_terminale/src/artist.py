import pymongo
from geopy.geocoders import Nominatim
from rich.console import Console
from rich.table import Table
from utils import get_db
import uuid

console = Console()

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
            console.print(f"[red]Impossibile trovare le coordinate per {location_nome}[/red]")
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

    artista_doc = db.artisti.find_one({"nome": username})
    if not artista_doc:
        console.print("[red]Errore: Artista non trovato.[/red]")
        return

    artista_id = artista_doc["_id"]

    concerto = {
        "nome": nome_concerto,
        "data": data,
        "artista_id": artista_id,
        "location_id": location_id,
        "settori": settori
    }

    db.concerti.insert_one(concerto)
    console.print("[green]Concerto creato con successo![/green]")

def visualizza_situazione_biglietti(username):
    db = get_db()
    artista_doc = db.artisti.find_one({"nome": username})
    if not artista_doc:
        console.print("[red]Nessun artista trovato con questo nome.[/red]")
        return
    
    artista_id = artista_doc["_id"]
    concerti = list(db.concerti.find({"artista_id": artista_id}))
    
    if len(concerti) == 0:
        console.print("[red]Nessun concerto trovato per l'artista.[/red]")
        return
    
    table = Table(title="Situazione Biglietti")
    table.add_column("Concerto", style="cyan")
    table.add_column("Data", style="magenta")
    table.add_column("Settore", style="green")
    table.add_column("Posti Rimanenti", style="red")

    for concerto in concerti:
        for settore in concerto['settori']:
            table.add_row(concerto['nome'], concerto['data'], settore['nome'], str(settore['posti_disponibili']))
    
    console.print(table)
            
def duplica_concerto(username):
    db = get_db()
    artista_doc = db.artisti.find_one({"nome": username})
    if not artista_doc:
        console.print("[red]Nessun artista trovato con questo nome.[/red]")
        return
    
    artista_id = artista_doc["_id"]
    concerti = list(db.concerti.find({"artista_id": artista_id}))
    
    if not concerti:
        console.print("[red]Nessun concerto trovato per l'artista.[/red]")
        return
    
    table = Table(title="Concerti Disponibili")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Concerto", style="magenta")
    table.add_column("Data", style="green")

    for idx, concerto in enumerate(concerti):
        table.add_row(str(idx + 1), concerto['nome'], concerto['data'])
    
    console.print(table)

    try:
        scelta = int(input("Quale concerto vuoi duplicare? ")) - 1
        if scelta < 0 or scelta >= len(concerti):
            console.print("[red]Scelta non valida.[/red]")
            return
    except ValueError:
        console.print("[red]Inserisci un valore numerico valido.[/red]")
        return

    nuova_data = input("Inserisci la nuova data (AAAA-MM-GG): ")
    
    concerto_da_duplicare = concerti[scelta]
    nuovo_concerto = concerto_da_duplicare.copy()
    nuovo_concerto['_id'] = str(uuid.uuid4())  # Genera un nuovo ID unico per il concerto duplicato
    nuovo_concerto['data'] = nuova_data
    
    db.concerti.insert_one(nuovo_concerto)
    console.print("[green]Concerto duplicato con successo![/green]")

def visualizza_utenti_biglietti(username):
    db = get_db()
    artista_doc = db.artisti.find_one({"nome": username})
    if not artista_doc:
        console.print("[red]Nessun artista trovato con questo nome.[/red]")
        return
    
    artista_id = artista_doc["_id"]
    concerti = list(db.concerti.find({"artista_id": artista_id}))
    
    if len(concerti) == 0:
        console.print("[red]Nessun concerto trovato per l'artista.[/red]")
        return
    
    table = Table(title="Utenti Biglietti")
    table.add_column("Concerto", style="cyan")
    table.add_column("Data", style="magenta")
    table.add_column("Utente", style="green")
    table.add_column("Settore", style="red")

    for concerto in concerti:
        utenti = list(db.utenti.find({"biglietti.concerto": concerto['nome']}))
        if len(utenti) == 0:
            console.print(f"[red]Nessun utente ha acquistato i biglietti per {concerto['nome']}.[/red]")
            continue
        for utente in utenti:
            biglietti_utente = [biglietto for biglietto in utente['biglietti'] if biglietto['concerto'] == concerto['nome']]
            for biglietto in biglietti_utente:
                table.add_row(concerto['nome'], concerto['data'], utente['username'], biglietto['settore'])
    
    console.print(table)
