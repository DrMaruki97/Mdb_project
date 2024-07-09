import os
from datetime import datetime

# Funzione per pulire lo schermo
def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:
        os.system('clear')  # Linux/Mac

# Funzione per cercare concerti
def cerca_concerto():
    clear_screen()
    print("Cerca un concerto")
    print("================")

    # Input dell'artista
    artista = input("Artista che partecipa al concerto: ")

    # Simuliamo la ricerca (puoi sostituire questa parte con la logica specifica al tuo caso)
    print(f"\nRisultati della ricerca per '{artista}':")
    print("===================================")
    # Simulazione dei risultati trovati
    print("Concerto 1: Artista - Ligabue, Nome - Campovolo 2024")
    print("Concerto 2: Artista - Vasco Rossi, Nome - Live Kom 2024")
    print("Concerto 3: Artista - Foo Fighters, Nome - World Tour 2024")

    input("\nPremi INVIO per continuare...")

# Funzione per inserire le informazioni del concerto
def concert_info_menu():
    concert_info = {}
    
    while True:
        print("\nOpzioni per inserire le informazioni del concerto:")
        print("1. Nome dell'artista")
        print("2. Nome del concerto")
        print("3. Data del concerto")
        print("4. Luogo del concerto")
        print("5. Torna al menu principale")
        
        choice = input("Scegli un'opzione: ")
        
        if choice == '1':
            concert_info['artista'] = input("Inserisci il nome dell'artista: ")
        elif choice == '2':
            concert_info['concerto'] = input("Inserisci il nome del concerto: ")
        elif choice == '3':
            concert_info['data'] = input("Inserisci la data del concerto: ")
        elif choice == '4':
            concert_info['luogo'] = input("Inserisci il luogo del concerto: ")
        elif choice == '5':
            print("Torna al menu principale.")
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
        print("2. Inserisci informazioni del concerto")
        print("3. Esci")
        
        scelta = input("\nInserisci il numero dell'opzione desiderata: ")

        if scelta == '1':
            cerca_concerto()
        elif scelta == '2':
            concert_info_menu()
        elif scelta == '3':
            print("\nGrazie per aver usato l'applicazione.")
            break
        else:
            print("\nOpzione non valida. Riprova.")
            input("\nPremi INVIO per continuare...")

if __name__ == "__main__":
    main_menu()
