import bcrypt
import pymongo

def get_db():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = pymongo.MongoClient(uri)
    return client["concerti_biglietti"]

def registra_utente(username, password, conferma_password, tipo):
    if password != conferma_password:
        print("Le password non corrispondono.")
        return False
    
    db = get_db()
    if db.utenti.find_one({"username": username}):
        print("Username già esistente.")
        return False
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.utenti.insert_one({"username": username, "password": hashed, "tipo": tipo, "saldo": 0, "biglietti": []})
    
    if tipo == "artista":
        artista_doc = db.artisti.find_one({"nome": username})
        if artista_doc:
            concerti = list(db.concerti.find({"artista_id": artista_doc["_id"]}))
            db.artisti.update_one({"_id": artista_doc["_id"]}, {"$set": {"utente": username}})
        else:
            db.artisti.insert_one({"_id": username, "nome": username})
            concerti = list(db.concerti.find({"artista_id": username}))
            if concerti:
                for concerto in concerti:
                    db.concerti.update_one({"_id": concerto["_id"]}, {"$set": {"artista_id": username}})
    
    print("Registrazione avvenuta con successo!")
    return True

def login_utente(username, password):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    
    if not utente:
        print("Username non trovato.")
        return False
    
    if bcrypt.checkpw(password.encode('utf-8'), utente["password"]):
        print("Login effettuato con successo!")
        return True
    else:
        print("Password errata.")
        return False
