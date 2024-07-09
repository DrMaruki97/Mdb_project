import os
from datetime import datetime
from pymongo import MongoClient

# Funzione per pulire lo schermo
def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:
        os.system('clear')  # Linux/Mac

# Funzione per connettersi a MongoDB
def connect_to_mongo():
    # Cambia l'URI con il tuo URI MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    return client

# Funzione per inserire le informazioni del concerto nel database
def insert_concert_info(concert_info):
    client = connect_to_mongo()
    db = client['concerts_db']
    collection = db['concerts']
    collection.insert_one(concert_info)
    client.close()

# Funzione per cercare il concerto
def concert_info_menu():
    concert_info = {}
    
    while True:
        print("\nOpzioni per inserire le informazioni del concerto:")
        print("1. Nome dell'artista")
        print("2. Nome del concerto")
        print("3. Data del concerto")
        print("4. Luogo del concerto")
        print("5. Salva e torna al menu principale")
        
        choice = input("Scegli un'opzione: ")
        clear_screen()
        
        if choice == '1':
            concert_info['artista'] = input("Inserisci il nome dell'artista: ")
        elif choice == '2':
            concert_info['concerto'] = input("Inserisci il nome del concerto: ")
        elif choice == '3':
            concert_info['data'] = input("Inserisci la data del concerto (YYYY-MM-DD): ")
        elif choice == '4':
            concert_info['luogo'] = input("Inserisci il luogo del concerto: ")
        elif choice == '5':
            if 'data' in concert_info:
                try:
                    concert_info['data'] = datetime.strptime(concert_info['data'], "%Y-%m-%d")
                except ValueError:
                    print("Formato data non valido. Usa il formato YYYY-MM-DD.")
                    continue
            insert_concert_info(concert_info)
            print("Informazioni del concerto salvate con successo!")
            break
        else:
            print("Scelta non valida. Riprova.")
        
        print("\nInformazioni del concerto attuali:")
        for key, value in concert_info.items():
            print(f"{key.capitalize()}: {value}")

# Funzione principale del menu
def main_menu():
    while True:
        clear_screen()
        print("Benvenuto!")
        print("===========")
        print("Opzioni disponibili:")
        print("1. Cerca concerto")
        print("2. Esci")
        
        scelta = input("\nInserisci il numero dell'opzione desiderata: ")
        clear_screen()

        if scelta == '1':
            concert_info_menu()
        elif scelta == '2':
            print("\nGrazie per aver usato l'applicazione.")
            break
        else:
            print("\nOpzione non valida. Riprova.")
            input("\nPremi INVIO per continuare...")

if __name__ == "__main__":
    main_menu()
