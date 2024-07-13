import pymongo
import bcrypt
from rich.console import Console
from rich.table import Table

console = Console()

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
        concerti_acquistati = list(set([biglietto.get('concerto', 'N/A') for biglietto in biglietti]))
        table = Table(title="Concerti acquistati")
        table.add_column("Index", justify="right", style="cyan", no_wrap=True)
        table.add_column("Concerto", style="magenta")
        
        for idx, concerto in enumerate(concerti_acquistati):
            table.add_row(str(idx + 1), concerto)
        
        console.print(table)
        
        try:
            scelta = int(input("Per quale concerto vuoi vedere i biglietti? ")) - 1
        except ValueError:
            console.print("Inserisci un valore numerico valido.", style="red")
            return

        if scelta < 0 or scelta >= len(concerti_acquistati):
            console.print("Scelta non valida.", style="red")
            return

        concerto_scelto = concerti_acquistati[scelta]
        biglietti_concerto = [biglietto for biglietto in biglietti if biglietto.get('concerto', 'N/A') == concerto_scelto]

        table = Table(title=f"Biglietti per {concerto_scelto}")
        table.add_column("Codice", style="cyan")
        table.add_column("Data", style="magenta")
        table.add_column("Settore", style="green")
        table.add_column("Prezzo", justify="right", style="red")

        for biglietto in biglietti_concerto:
            codice = biglietto.get('codice', 'N/A')
            data = biglietto.get('data', 'N/A')
            settore = biglietto.get('settore', 'N/A')
            prezzo = biglietto.get('prezzo', 'N/A')
            table.add_row(codice, data, settore, f"{prezzo}€")
        
        console.print(table)
    else:
        console.print("Non hai biglietti acquistati.", style="red")