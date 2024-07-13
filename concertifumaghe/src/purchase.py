import pymongo
import uuid
from utils import get_db

def acquista_biglietti(username, concerti=None):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    
    if not utente:
        print("Errore: utente non trovato.")
        return

    if not concerti:
        concerti = list(db.concerti.find({}))

    if not concerti:
        print("Nessun concerto disponibile per l'acquisto.")
        return

    print("Concerti disponibili per l'acquisto:")
    for idx, concerto in enumerate(concerti):
        print(f"{idx+1}: {concerto['nome']}, {concerto['data']}, Artista: {concerto['artista_id']}, Location: {concerto['location_id']}")
        for settore in concerto['settori']:
            print(f"    Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

    try:
        scelta_concerto = int(input("Per quale concerto vuoi acquistare? ")) - 1
        if scelta_concerto < 0 or scelta_concerto >= len(concerti):
            print("Scelta non valida.")
            return
    except ValueError:
        print("Inserisci un valore numerico valido.")
        return

    concerto_scelto = concerti[scelta_concerto]

    print("Settori disponibili:")
    for idx, settore in enumerate(concerto_scelto['settori']):
        print(f"{idx+1}: Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

    try:
        scelta_settore = int(input("Per quale settore vuoi acquistare? ")) - 1
        if scelta_settore < 0 or scelta_settore >= len(concerto_scelto['settori']):
            print("Scelta non valida.")
            return
    except ValueError:
        print("Inserisci un valore numerico valido.")
        return

    settore_scelto = concerto_scelto['settori'][scelta_settore]

    try:
        quantita = int(input("Quanti biglietti? "))
        if quantita < 1 or quantita > settore_scelto['posti_disponibili']:
            print("Quantità non valida.")
            return
    except ValueError:
        print("Inserisci un valore numerico valido.")
        return

    # Aggiorna i posti disponibili
    settore_scelto['posti_disponibili'] -= quantita

    # Genera i biglietti e salva nel profilo utente
    biglietti = []
    for _ in range(quantita):
        biglietto = {
            "id": str(uuid.uuid4()),
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

    print(f"I tuoi biglietti per un totale di {settore_scelto['prezzo'] * quantita}€:")
    for biglietto in biglietti:
        print(f"Codice: {biglietto['id']}, {biglietto['concerto']}, {biglietto['data']}, Settore: {biglietto['settore']}, Prezzo: {biglietto['prezzo']}€")
    print(f"Saldo rimanente: {utente['saldo'] - settore_scelto['prezzo'] * quantita}€")

    db.utenti.update_one(
        {"username": username},
        {"$inc": {"saldo": -settore_scelto['prezzo'] * quantita}}
    )
