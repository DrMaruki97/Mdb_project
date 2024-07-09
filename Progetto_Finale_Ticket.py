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
    print(f"\nRisultati della ricerca per '{artista}' e '{nome_concerto}':")
    print("===================================")
    # Simulazione dei risultati trovati
    print("Concerto 1: Artista - Ligabue, Nome - Campovolo 2024")
    print("Concerto 2: Artista - Vasco Rossi, Nome - Live Kom 2024")
    print("Concerto 3: Artista - Foo Fighters, Nome - World Tour 2024")

    input("\nPremi INVIO per continuare...")

# Funzione per avviare la sessione
def avvia_sessione():
    while True:
        clear_screen()
        print("Benvenuto!")
        print("===========")
        print("Opzioni disponibili:")
        print("1. Cerca concerto")
        print("2. Esci")

        scelta = input("\nInserisci il numero dell'opzione desiderata: ")

        if scelta == '1':
            cerca_concerto()
        elif scelta == '2':
            print("\nGrazie per aver usato l'applicazione.")
            break
        else:
            print("\nOpzione non valida. Riprova.")
            input("\nPremi INVIO per continuare...")

if __name__ == "__main__":
    avvia_sessione()
