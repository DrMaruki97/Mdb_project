import pymongo
import uuid
import bcrypt
from auth import get_db
from rich.console import Console
from rich.table import Table
from rich.style import Style
from profile import rimuovi_saldo, aggiungi_saldo

console = Console()

def acquista_biglietti(username, concerti=None):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    
    if not utente:
        console.print("[red]Errore: utente non trovato.[/red]")
        return

    if not concerti:
        concerti = list(db.concerti.find({}))

    if not concerti:
        console.print("[red]Nessun concerto disponibile per l'acquisto.[/red]")
        return

    table = Table(title="Concerti disponibili per l'acquisto")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Concerto", style="magenta")
    table.add_column("Data", style="green")
    table.add_column("Artista", style="blue")
    table.add_column("Location", style="blue")

    sold_out_style = Style(color="red", strike=True)

    for idx, concerto in enumerate(concerti):
        artista = db.artisti.find_one({"_id": concerto['artista_id']})
        location = db.location.find_one({"_id": concerto['location_id']})
        artista_nome = artista['nome'] if artista else 'N/A'
        location_nome = location['nome'] if location else 'N/A'
        
        table.add_row(str(idx + 1), concerto['nome'], concerto['data'], artista_nome, location_nome)
        for settore in concerto['settori']:
            if settore['posti_disponibili'] == 0:
                table.add_row("", f"Settore: {settore['nome']}", f"Prezzo: {settore['prezzo']}€", "Sold Out", style=sold_out_style)
            else:
                table.add_row("", f"Settore: {settore['nome']}", f"Prezzo: {settore['prezzo']}€", f"Posti disponibili: {settore['posti_disponibili']}")
    
    console.print(table)

    while True:
        try:
            scelta_concerto = int(input("Per quale concerto vuoi acquistare? ")) - 1
            if scelta_concerto < 0 or scelta_concerto >= len(concerti):
                console.print("[red]Scelta non valida.[/red]")
            else:
                break
        except ValueError:
            console.print("[red]Inserisci un valore numerico valido.[/red]")

    concerto_scelto = concerti[scelta_concerto]

    table = Table(title="Settori disponibili")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Settore", style="magenta")
    table.add_column("Prezzo", style="green")
    table.add_column("Posti disponibili", style="red")

    for idx, settore in enumerate(concerto_scelto['settori']):
        if settore['posti_disponibili'] == 0:
            table.add_row(str(idx + 1), settore['nome'], f"{settore['prezzo']}€", "Sold Out", style=sold_out_style)
        else:
            table.add_row(str(idx + 1), settore['nome'], f"{settore['prezzo']}€", str(settore['posti_disponibili']))

    console.print(table)

    while True:
        try:
            scelta_settore = int(input("Per quale settore vuoi acquistare? ")) - 1
            if scelta_settore < 0 or scelta_settore >= len(concerto_scelto['settori']):
                console.print("[red]Scelta non valida.[/red]")
            else:
                break
        except ValueError:
            console.print("[red]Inserisci un valore numerico valido.[/red]")

    settore_scelto = concerto_scelto['settori'][scelta_settore]

    if settore_scelto['posti_disponibili'] == 0:
        console.print("[red]Questo settore è sold out.[/red]")
        return

    while True:
        try:
            quantita = int(input("Quanti biglietti? "))
            if quantita < 1 or quantita > settore_scelto['posti_disponibili']:
                console.print("[red]Quantità non valida.[/red]")
            else:
                break
        except ValueError:
            console.print("[red]Inserisci un valore numerico valido.[/red]")

    costo_totale = settore_scelto['prezzo'] * quantita

    if utente['saldo'] < costo_totale:
        console.print("[red]Saldo insufficiente per completare l'acquisto. Aggiungi fondi al tuo saldo.[/red]")
        return

    if not rimuovi_saldo(username, costo_totale):
        return

    # Aggiorna i posti disponibili
    settore_scelto['posti_disponibili'] -= quantita

    biglietti = []
    for _ in range(quantita):
        biglietto = {
            "codice": str(uuid.uuid4()),
            "concerto": concerto_scelto['nome'],
            "data": concerto_scelto['data'],
            "settore": settore_scelto['nome'],
            "prezzo": settore_scelto['prezzo']
        }
        biglietti.append(biglietto)

    db.utenti.update_one(
        {"username": username},
        {"$push": {"biglietti": {"$each": biglietti}}}
    )

    # Aggiorna il concerto nel database
    db.concerti.update_one(
        {"_id": concerto_scelto["_id"], "settori.nome": settore_scelto['nome']},
        {"$set": {"settori.$.posti_disponibili": settore_scelto['posti_disponibili']}}
    )

    table = Table(title="Biglietti acquistati")
    table.add_column("Codice", style="cyan")
    table.add_column("Concerto", style="magenta")
    table.add_column("Data", style="green")
    table.add_column("Settore", style="blue")
    table.add_column("Prezzo", style="red")

    for biglietto in biglietti:
        table.add_row(biglietto['codice'], biglietto['concerto'], biglietto['data'], biglietto['settore'], f"{biglietto['prezzo']}€")

    console.print(table)
    console.print(f"[green]Saldo rimanente: {utente['saldo'] - costo_totale}€[/green]")

    # Gestione del saldo dell'artista
    artista = db.artisti.find_one({"_id": concerto_scelto['artista_id']})
    artista_nome = artista['nome'] if artista else 'N/A'
    artista_utente = db.utenti.find_one({"username": artista_nome})
    
    if artista_utente:
        aggiungi_saldo(artista_nome, costo_totale)
    else:
        # Creare un nuovo account per l'artista con password predefinita "123"
        hashed_password = bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt())
        nuovo_artista_utente = {
            "username": artista_nome,
            "password": hashed_password,
            "saldo": costo_totale,
            "tipo": "artista"
        }
        db.utenti.insert_one(nuovo_artista_utente)
        console.print(f"[green]Creato nuovo account per l'artista {artista_nome} con saldo iniziale di {costo_totale}€ e password predefinita '123'[/green]")
