import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import time
from fuzzywuzzy import process

# Connessione iniziale a MongoDB
uri = "mongodb+srv://mongo:mongo@ufs13.9ag482l.mongodb.net/?retryWrites=true&w=majority&appName=UFS13"
client = MongoClient(uri, server_api=ServerApi('1'))

# Funzione per ottenere il riferimento al database e alla collezione
def get_collection():
    db = client['Mongo_DB_Data_Lake']
    collection = db['Concerti']
    return collection

# Funzione per pulire lo schermo
def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:
        os.system('clear')  # Linux/Mac

# Funzione per cercare i concerti per artista
def search_concerts_by_artist(artist_name):
    collection = get_collection()
    concerts = collection.find({"artisiti": artist_name})
    return concerts

# Funzione per cercare i concerti per nome del concerto
def search_concerts_by_name(concert_name):
    collection = get_collection()
    concerts = collection.find({"nome": concert_name})
    return concerts

# Funzione per cercare i concerti per località
def search_concerts_by_location(location_name):
    collection = get_collection()
    concerts = collection.find({"nome_luogo": location_name})
    return concerts

# Funzione per cercare artisti simili
def find_similar_artist(artist_name): 
    collection = get_collection()
    artists = collection.distinct("artisiti")
    similar_artist, score = process.extractOne(artist_name, artists)
    if score >= 80:  # 80% di somiglianza 
        print(f"Forse stavi cercando {similar_artist}")
        time.sleep(5)
        return similar_artist
    return None

# Funzione per cercare nomi di concerti simili
def find_similar_concert_name(concert_name):
    collection = get_collection()
    concert_names = collection.distinct("nome")
    similar_concert, score = process.extractOne(concert_name, concert_names)
    if score >= 80:  # 80% di somiglianza
        print(f"Forse stavi cercando {similar_concert}")
        time.sleep(5)
        return similar_concert
    return None

# Funzione per visualizzare i concerti trovati
def display_concerts(concerts):
    found = False
    for concert in concerts:
        found = True
        print("\nArtista: ", concert['artisiti'])
        print("Concerto: ", concert['nome'])
        print("Data: ", concert['date'][0].strftime('%y-%m-%d'))
        print("Luogo: ", concert['nome_luogo'])
        print("--------------")
    
    if not found:
        print("Nessun concerto trovato per la ricerca specificata.")

# Funzione per cercare concerti
def search_concerts_menu():
    while True:
        clear_screen()
        print("Cerca concerti")
        print("==============")
        print("1. Cerca per artista")
        print("2. Cerca per nome del concerto")
        print("3. Cerca per località")
        print("4. Torna al menu principale")
        
        scelta = input("\nInserisci il numero dell'opzione desiderata: ")
        clear_screen()
        
        if scelta == '1':
            artist_name = input("Inserisci il nome dell'artista da cercare: ")
            collection = get_collection()
            concerts = search_concerts_by_artist(artist_name)
            if collection.count_documents({"artisiti": artist_name}) == 0:
                similar_artist = find_similar_artist(artist_name)
                if similar_artist:
                    concerts = search_concerts_by_artist(similar_artist)
            clear_screen()
            display_concerts(concerts)
            input("\nPremi INVIO per tornare al menu di ricerca...")

        elif scelta == '2':
            concert_name = input("Inserisci il nome del concerto da cercare: ")
            collection = get_collection()
            concerts = search_concerts_by_name(concert_name)
            if collection.count_documents({"nome": concert_name}) == 0:
                similar_concert = find_similar_concert_name(concert_name)
                if similar_concert:
                    concerts = search_concerts_by_name(similar_concert)
            clear_screen()
            display_concerts(concerts)
            input("\nPremi INVIO per tornare al menu di ricerca...")

        elif scelta == '3':
            location_name = input("Inserisci la località del concerto da cercare: ")
            collection = get_collection()
            concerts = search_concerts_by_location(location_name)
            clear_screen()
            display_concerts(concerts)
            input("\nPremi INVIO per tornare al menu di ricerca...")

        elif scelta == '4':
            break

        else:
            print("\nOpzione non valida. Riprova.")
            input("\nPremi INVIO per continuare...")

# Funzione principale del menu
def main_menu():
    while True:
        clear_screen()
        print("Benvenuto!")
        print("===========")
        print("Opzioni disponibili:")
        print("1. Cerca concerti")
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
