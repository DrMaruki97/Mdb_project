import pymongo

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
        print(f"{idx+1}: {concerto.get('nome')}, {concerto.get('data')}, disp:{concerto.get('disp', 'N/A')}, {concerto.get('prezzo', 'N/A')}€, Artista: {artista.get('nome', 'N/A')}, Location: {location.get('nome', 'N/A')}")

    try:
        concerto_id = int(input("Per quale concerto vuoi acquistare? ")) - 1
        quantita = int(input("Quanti biglietti? "))
    except ValueError:
        print("Inserisci un valore numerico valido.")
        return

    if concerto_id < 0 or concerto_id >= len(concerti):
        print("Concerto non valido.")
        return

    concerto = concerti[concerto_id]
    disponibilita = concerto.get('disp', 0)
    prezzo_totale = concerto.get('prezzo', 0) * quantita

    utente = db.utenti.find_one({"username": username})
    saldo = utente.get("saldo", 0)

    if disponibilita >= quantita:
        if saldo >= prezzo_totale:
            db.concerti.update_one(
                {"_id": concerto["_id"]},
                {"$inc": {"disp": -quantita}}
            )
            db.utenti.update_one(
                {"username": username},
                {
                    "$inc": {"saldo": -prezzo_totale},
                    "$push": {
                        "biglietti": {
                            "concerto": concerto.get('nome'),
                            "data": concerto.get('data'),
                            "quantita": quantita
                        }
                    }
                }
            )
            print(f"I tuoi biglietti per un totale di {prezzo_totale}€:")
            for i in range(quantita):
                print(f"{concerto.get('nome')}, {concerto.get('data')}, n.{concerto['_id']}-{i+1}")
            print(f"Disponibilità aggiornata: {disponibilita - quantita}")
            print(f"Saldo rimanente: {saldo - prezzo_totale}€")
        else:
            print("Saldo insufficiente.")
    else:
        print("Disponibilità insufficiente")
