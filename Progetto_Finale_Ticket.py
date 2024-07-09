import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Connessione iniziale a MongoDB
# Cambia l'URI con il tuo URI MongoDB
uri = "mongodb+srv://mongo:mongo@ufs13.9ag482l.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
client = MongoClient(uri, server_api=ServerApi('1'))

# Funzione per pulire lo schermo
def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:
        os.system('clear')  # Linux/Mac

# Funzione per cercare i concerti per artista
def search_concerts_by_artist(artist_name):
    db = client['Mongo_DB_Data_Lake']
    collection = db['Concerti']
    concerts = collection.find({"artisiti": artist_name})
    return concerts

# Funzione per visualizzare i concerti trovati
def display_concerts(concerts):
    for concert in concerts:
        print("\nArtista: ", concert['artisiti'])
        print("Concerto: ", concert['nome'])
        print("Data: ", concert['date'][0].strftime('%y-%m-%d'))
        print("Luogo: ", concert['nome_luogo'])
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
