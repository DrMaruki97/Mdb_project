import bcrypt
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from rich.console import Console

console = Console()

def get_db():
    uri = "mongodb+srv://lucagiovagnoli:t7g%5EFyi7zpN!Liw@ufs13.dsmvdrx.mongodb.net/"
    client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
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
        pipeline = [
            {"$match": {"nome": username}},
            {"$lookup": {
                "from": "concerti",
                "localField": "_id",
                "foreignField": "artista_id",
                "as": "concerti"
            }}
        ]
        artista_docs = list(db.artisti.aggregate(pipeline))
        
        if artista_docs:
            artista_doc = artista_docs[0]
            artista_id = artista_doc["_id"]
            db.artisti.update_one({"_id": artista_id}, {"$set": {"utente": username}})
            for concerto in artista_doc["concerti"]:
                db.concerti.update_one({"_id": concerto["_id"]}, {"$set": {"artista_id": artista_id}})
        else:
            artista_id = username
            db.artisti.insert_one({"_id": artista_id, "nome": username})
    
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
