import bcrypt
import pymongo
from rich.console import Console

console = Console()

def get_db():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = pymongo.MongoClient(uri)
    return client["concerti_biglietti"]

def registra_utente(username, password, conferma_password, tipo):
    if password != conferma_password:
        console.print("[red]Le password non corrispondono.[/red]")
        return False
    
    db = get_db()
    if db.utenti.find_one({"username": username}):
        console.print("[red]Username già esistente.[/red]")
        return False
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.utenti.insert_one({"username": username, "password": hashed, "tipo": tipo, "saldo": 0, "biglietti": []})
    
    if tipo == "artista":
        artista_doc = db.artisti.find_one({"nome": username})
        if artista_doc:
            artista_id = artista_doc["_id"]
            concerti = list(db.concerti.find({"artista_id": artista_id}))
            db.artisti.update_one({"_id": artista_id}, {"$set": {"utente": username}})
        else:
            artista_id = username
            db.artisti.insert_one({"_id": artista_id, "nome": username})
            concerti = list(db.concerti.find({"artista_id": artista_id}))
            if concerti:
                for concerto in concerti:
                    db.concerti.update_one({"_id": concerto["_id"]}, {"$set": {"artista_id": artista_id}})
    
    console.print("[green]Registrazione avvenuta con successo![/green]")
    return True

def login_utente(username, password):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    
    if not utente:
        console.print("[red]Username non trovato.[/red]")
        return False
    
    if bcrypt.checkpw(password.encode('utf-8'), utente["password"]):
        console.print("[green]Login effettuato con successo![/green]")
        return True
    else:
        console.print("[red]Password errata.[/red]")
        return False
