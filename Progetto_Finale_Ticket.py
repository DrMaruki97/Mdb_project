import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Funzione per pulire lo schermo
def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:
        os.system('clear')  # Linux/Mac

# Funzione per connettersi a MongoDB
def connect_to_mongo():
    # Cambia l'URI con il tuo URI MongoDB
    uri = "mongodb+srv://<username>:<password>@ufs13.9ag482l.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    
    return client

# Funzione per cercare i concerti per artista
def search_concerts_by_artist(artist_name):
    client = connect_to_mongo()
    db = client['concerts_db']
    collection = db['concerts']
    concerts = collection.find({"artista": artist_name})
    client.close()
    return concerts

# Funzione per visualizzare i concerti trovati
def display_concerts(concerts):
    for concert in concerts:
        print("\nArtista: ", concert.get('artista', 'N/A'))
        print("Concerto: ", concert.get('concerto', 'N/A'))
        print("Data: ", concert.get('data', 'N/A').strftime("%Y-%m-%d") if concert.get('data') else 'N/A')
        print("Luogo: ", concert.get('luogo', 'N/A'))
        print("--------------")

# Funzione per cercare concerti
def search_concerts_menu():
    artist_name = input("Inserisci il nome dell'artista da cercare: ")
    concerts = search_concerts_by_artist(artist_name)
    clear_screen()
    display_concerts(concerts)
    input("\nPremi INVIO per tornare al menu principale...")

# Funzione principale del menu
def main_menu():
    while True:
        clear_screen()
        print("Benvenuto!")
        print("===========")
        print("Opzioni disponibili:")
        print("1. Cerca concerti per artista")
        print("2. Esci")
        
        scelta = input("\nInserisci il numero dell'opzione desiderata: ")
        clear_screen()

        if scelta == '1':
            search_concerts_menu()
        elif scelta == '2':
            print("\nGrazie per aver usato l'applicazione.")
            break
        else:
            print("\nOpzione non valida. Riprova.")
            input("\nPremi INVIO per continuare...")

if __name__ == "__main__":
    main_menu()

abracadabra