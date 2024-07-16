import pymongo
from geopy.geocoders import Nominatim
from rich.console import Console
from rich.table import Table
from rich.style import Style
from auth import get_db
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
    concerti = list(db.concerti.aggregate([
        {"$match": {"artista_id": artista_id}},
        {"$unwind": "$settori"},
        {"$project": {
            "nome": 1,
            "data": 1,
            "settore_nome": "$settori.nome",
            "posti_rimanenti": "$settori.posti_disponibili"
        }}
    ]))
    
    if len(concerti) == 0:
        console.print("[red]Nessun concerto trovato per l'artista.[/red]")
        return
    
    table = Table(title="Situazione Biglietti")
    table.add_column("Concerto", style="cyan")
    table.add_column("Data", style="magenta")
    table.add_column("Settore", style="green")
    table.add_column("Posti Rimanenti", style="red")

    sold_out_style = Style(color="red", strike=True)

    for concerto in concerti:
        posti_rimanenti = concerto['posti_rimanenti']
        if posti_rimanenti == 0:
            table.add_row(concerto['nome'], concerto['data'], concerto['settore_nome'], "Sold Out", style=sold_out_style)
        else:
            table.add_row(concerto['nome'], concerto['data'], concerto['settore_nome'], str(posti_rimanenti))
    
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
    concerti = list(db.concerti.aggregate([
        {"$match": {"artista_id": artista_id}},
        {"$lookup": {
            "from": "utenti",
            "localField": "nome",
            "foreignField": "biglietti.concerto",
            "as": "utenti"
        }},
        {"$unwind": "$utenti"},
        {"$unwind": "$utenti.biglietti"},
        {"$match": {"utenti.biglietti.concerto": {"$exists": True, "$eq": "$nome"}}},
        {"$project": {
            "concerto_nome": "$nome",
            "concerto_data": "$data",
            "utente_nome": "$utenti.username",
            "settore_nome": "$utenti.biglietti.settore"
        }}
    ]))
    
    if len(concerti) == 0:
        console.print("[red]Nessun utente ha acquistato i biglietti per i concerti dell'artista.[/red]")
        return
    
    table = Table(title="Utenti Biglietti")
    table.add_column("Concerto", style="cyan")
    table.add_column("Data", style="magenta")
    table.add_column("Utente", style="green")
    table.add_column("Settore", style="red")

    for concerto in concerti:
        table.add_row(concerto['concerto_nome'], concerto['concerto_data'], concerto['utente_nome'], concerto['settore_nome'])
    
    console.print(table)
