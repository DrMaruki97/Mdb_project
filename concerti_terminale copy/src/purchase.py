import pymongo
import uuid
from utils import get_db
from rich.console import Console
from rich.table import Table

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

    for idx, concerto in enumerate(concerti):
        table.add_row(str(idx + 1), concerto['nome'], concerto['data'], concerto['artista_id'], concerto['location_id'])
        for settore in concerto['settori']:
            table.add_row("", f"Settore: {settore['nome']}", f"Prezzo: {settore['prezzo']}€", f"Posti disponibili: {settore['posti_disponibili']}")
    
    console.print(table)

    try:
        scelta_concerto = int(input("Per quale concerto vuoi acquistare? ")) - 1
        if scelta_concerto < 0 or scelta_concerto >= len(concerti):
            console.print("[red]Scelta non valida.[/red]")
            return
    except ValueError:
        console.print("[red]Inserisci un valore numerico valido.[/red]")
        return

    concerto_scelto = concerti[scelta_concerto]

    table = Table(title="Settori disponibili")
    table.add_column("Index", justify="right", style="cyan", no_wrap=True)
    table.add_column("Settore", style="magenta")
    table.add_column("Prezzo", style="green")
    table.add_column("Posti disponibili", style="red")

    for idx, settore in enumerate(concerto_scelto['settori']):
        table.add_row(str(idx + 1), settore['nome'], f"{settore['prezzo']}€", str(settore['posti_disponibili']))

    console.print(table)

    try:
        scelta_settore = int(input("Per quale settore vuoi acquistare? ")) - 1
        if scelta_settore < 0 or scelta_settore >= len(concerto_scelto['settori']):
            console.print("[red]Scelta non valida.[/red]")
            return
    except ValueError:
        console.print("[red]Inserisci un valore numerico valido.[/red]")
        return

    settore_scelto = concerto_scelto['settori'][scelta_settore]

    try:
        quantita = int(input("Quanti biglietti? "))
        if quantita < 1 or quantita > settore_scelto['posti_disponibili']:
            console.print("[red]Quantità non valida.[/red]")
            return
    except ValueError:
        console.print("[red]Inserisci un valore numerico valido.[/red]")
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
    console.print(f"[green]Saldo rimanente: {utente['saldo'] - settore_scelto['prezzo'] * quantita}€[/green]")

    db.utenti.update_one(
        {"username": username},
        {"$inc": {"saldo": -settore_scelto['prezzo'] * quantita}}
    )
