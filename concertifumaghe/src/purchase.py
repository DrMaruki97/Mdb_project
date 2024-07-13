import pymongo
import uuid

def get_db():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = pymongo.MongoClient(uri)
    return client["concerti_biglietti"]

def acquista_biglietti(username, concerti=None):
    db = get_db()
    if concerti is None:
        concerti = list(db.concerti.find())

    if not concerti:
        print("Nessun concerto disponibile per l'acquisto.")
        return

    print("Concerti disponibili per l'acquisto:")
    for idx, concerto in enumerate(concerti):
        location = db.location.find_one({"_id": concerto["location_id"]})
        artista = db.artisti.find_one({"_id": concerto["artista_id"]})
        settori = concerto.get('settori', [])
        print(f"{idx+1}: {concerto.get('nome')}, {concerto.get('data')}, Artista: {artista.get('nome', 'N/A')}, Location: {location.get('nome', 'N/A')}")
        for settore in settori:
            print(f"    Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

    try:
        concerto_id = int(input("Per quale concerto vuoi acquistare? ")) - 1
        settore_id = int(input("Per quale settore vuoi acquistare? ")) - 1
        quantita = int(input("Quanti biglietti? "))
    except ValueError:
        print("Inserisci un valore numerico valido.")
        return

    if concerto_id < 0 or concerto_id >= len(concerti):
        print("Concerto non valido.")
        return

    concerto = concerti[concerto_id]
    settore = concerto['settori'][settore_id]
    disponibilita = settore.get('posti_disponibili', 0)
    prezzo_totale = settore.get('prezzo', 0) * quantita

    utente = db.utenti.find_one({"username": username})
    saldo = utente.get("saldo", 0)

    if disponibilita >= quantita:
        if saldo >= prezzo_totale:
            db.concerti.update_one(
                {"_id": concerto["_id"], "settori.nome": settore['nome']},
                {"$inc": {"settori.$.posti_disponibili": -quantita}}
            )
            biglietti = []
            for i in range(quantita):
                codice_biglietto = str(uuid.uuid4())
                biglietti.append({
                    "codice": codice_biglietto,
                    "concerto": concerto.get('nome'),
                    "data": concerto.get('data'),
                    "settore": settore['nome'],
                    "prezzo": settore['prezzo']
                })
            db.utenti.update_one(
                {"username": username},
                {
                    "$inc": {"saldo": -prezzo_totale},
                    "$push": {"biglietti": {"$each": biglietti}}
                }
            )
            print(f"I tuoi biglietti per un totale di {prezzo_totale}€:")
            for biglietto in biglietti:
                print(f"Codice: {biglietto['codice']}, {biglietto['concerto']}, {biglietto['data']}, Settore: {biglietto['settore']}, Prezzo: {biglietto['prezzo']}€")
            print(f"Saldo rimanente: {saldo - prezzo_totale}€")
        else:
            print("Saldo insufficiente.")
    else:
        print("Disponibilità insufficiente")
