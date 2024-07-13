import pymongo
import uuid
from utils import get_db
from rich.console import Console

console = Console()

def acquista_biglietti(username, concerti=None):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    
    if not utente:
        console.print("Errore: utente non trovato.", style="red")
        return

    if not concerti:
        concerti = list(db.concerti.find({}))

    if not concerti:
        console.print("Nessun concerto disponibile per l'acquisto.", style="red")
        return

    console.print("Concerti disponibili per l'acquisto:", style="cyan")
    for idx, concerto in enumerate(concerti):
        console.print(f"{idx+1}: {concerto['nome']}, {concerto['data']}, Artista: {concerto['artista_id']}, Location: {concerto['location_id']}")
        for settore in concerto['settori']:
            console.print(f"    Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

    try:
        scelta_concerto = int(input("Per quale concerto vuoi acquistare? ")) - 1
        if scelta_concerto < 0 or scelta_concerto >= len(concerti):
            console.print("Scelta non valida.", style="red")
            return
    except ValueError:
        console.print("Inserisci un valore numerico valido.", style="red")
        return

    concerto_scelto = concerti[scelta_concerto]

    console.print("Settori disponibili:", style="cyan")
    for idx, settore in enumerate(concerto_scelto['settori']):
        console.print(f"{idx+1}: Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

    try:
        scelta_settore = int(input("Per quale settore vuoi acquistare? ")) - 1
        if scelta_settore < 0 or scelta_settore >= len(concerto_scelto['settori']):
            console.print("Scelta non valida.", style="red")
            return
    except ValueError:
        console.print("Inserisci un valore numerico valido.", style="red")
        return

    settore_scelto = concerto_scelto['settori'][scelta_settore]

    try:
        quantita = int(input("Quanti biglietti? "))
        if quantita < 1 or quantita > settore_scelto['posti_disponibili']:
            console.print("Quantità non valida.", style="red")
            return
    except ValueError:
        console.print("Inserisci un valore numerico valido.", style="red")
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

    for biglietto in biglietti:
        console.print(f"I tuoi biglietti per un totale di {settore_scelto['prezzo']}€ ciascuno:", style="green")
        console.print(f"Codice: {biglietto['codice']}, {biglietto['concerto']}, {biglietto['data']}, Settore: {biglietto['settore']}, Prezzo: {biglietto['prezzo']}€")

    console.print(f"Saldo rimanente: {utente['saldo'] - settore_scelto['prezzo'] * quantita}€", style="green")

    db.utenti.update_one(
        {"username": username},
        {"$inc": {"saldo": -settore_scelto['prezzo'] * quantita}}
    )
