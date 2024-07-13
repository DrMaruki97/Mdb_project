import pymongo
import bcrypt

def get_db():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = pymongo.MongoClient(uri)
    return client["concerti_biglietti"]

def modifica_nome(username, nuovo_nome):
    db = get_db()
    db.utenti.update_one({"username": username}, {"$set": {"username": nuovo_nome}})
    print("Nome aggiornato con successo!")

def modifica_password(username, vecchia_password, nuova_password, conferma_password):
    if nuova_password != conferma_password:
        print("Le nuove password non corrispondono.")
        return
    
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    
    if bcrypt.checkpw(vecchia_password.encode('utf-8'), utente["password"]):
        hashed = bcrypt.hashpw(nuova_password.encode('utf-8'), bcrypt.gensalt())
        db.utenti.update_one({"username": username}, {"$set": {"password": hashed}})
        print("Password aggiornata con successo!")
    else:
        print("Vecchia password errata.")

def aggiungi_saldo(username, importo):
    db = get_db()
    db.utenti.update_one({"username": username}, {"$inc": {"saldo": importo}})
    print(f"{importo}€ aggiunti al saldo.")

def visualizza_biglietti(username):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    biglietti = utente.get("biglietti", [])
    if biglietti:
        concerti_acquistati = list(set([biglietto['concerto'] for biglietto in biglietti]))
        print("Concerti acquistati:")
        for idx, concerto in enumerate(concerti_acquistati):
            print(f"{idx+1}: {concerto}")
        
        try:
            scelta = int(input("Per quale concerto vuoi vedere i biglietti? ")) - 1
        except ValueError:
            print("Inserisci un valore numerico valido.")
            return

        if scelta < 0 or scelta >= len(concerti_acquistati):
            print("Scelta non valida.")
            return

        concerto_scelto = concerti_acquistati[scelta]
        biglietti_concerto = [biglietto for biglietto in biglietti if biglietto['concerto'] == concerto_scelto]

        print(f"Biglietti per {concerto_scelto}:")
        for biglietto in biglietti_concerto:
            print(f"Codice: {biglietto['codice']}, Data: {biglietto['data']}, Settore: {biglietto['settore']}, Prezzo: {biglietto['prezzo']}€")
    else:
        print("Non hai biglietti acquistati.")
