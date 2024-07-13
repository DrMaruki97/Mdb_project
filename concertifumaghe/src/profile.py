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
        print("I tuoi biglietti acquistati:")
        for biglietto in biglietti:
            print(f"Concerto: {biglietto['concerto']}, Data: {biglietto['data']}, Quantità: {biglietto['quantita']}")
    else:
        print("Non hai biglietti acquistati.")
