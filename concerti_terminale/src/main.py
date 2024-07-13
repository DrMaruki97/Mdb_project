from search import cerca_concerto, acquista_biglietti
from auth import registra_utente, login_utente
from profile import modifica_nome, modifica_password, aggiungi_saldo, visualizza_biglietti
from artist import crea_concerto, visualizza_situazione_biglietti, duplica_concerto, visualizza_utenti_biglietti
from utils import get_db

def main():
    username = None
    tipo = None
    
    while True:
        if not username:
            print("1: Registrati")
            print("2: Login")
            scelta = input("> ")

            if scelta == '1':
                username = input("Inserisci username: ")
                password = input("Inserisci password: ")
                conferma_password = input("Conferma password: ")
                tipo = input("Tipo di profilo (utente/artista): ")
                if registra_utente(username, password, conferma_password, tipo):
                    print("Registrazione avvenuta con successo!")
                else:
                    username = None
            elif scelta == '2':
                username = input("Inserisci username: ")
                password = input("Inserisci password: ")
                if login_utente(username, password):
                    db = get_db()
                    user_data = db.utenti.find_one({"username": username})
                    tipo = user_data.get("tipo", "utente")
                else:
                    username = None
        else:
            if tipo == "utente":
                print("1: Cerca Concerto")
                print("2: Acquista Biglietti")
                print("3: Profilo")
                print("4: Esci")
                scelta = input("> ")

                if scelta == '1':
                    cerca_concerto(username)
                elif scelta == '2':
                    acquista_biglietti(username)
                elif scelta == '3':
                    while True:
                        print("1: Modifica Nome")
                        print("2: Modifica Password")
                        print("3: Aggiungi Saldo")
                        print("4: Visualizza Biglietti")
                        print("5: Torna al menu principale")
                        scelta_profilo = input("> ")

                        if scelta_profilo == '1':
                            nuovo_nome = input("Inserisci il nuovo nome: ")
                            modifica_nome(username, nuovo_nome)
                            username = nuovo_nome
                        elif scelta_profilo == '2':
                            vecchia_password = input("Inserisci la vecchia password: ")
                            nuova_password = input("Inserisci la nuova password: ")
                            conferma_password = input("Conferma la nuova password: ")
                            modifica_password(username, vecchia_password, nuova_password, conferma_password)
                        elif scelta_profilo == '3':
                            try:
                                importo = int(input("Inserisci l'importo da aggiungere: "))
                                aggiungi_saldo(username, importo)
                            except ValueError:
                                print("Inserisci un valore numerico valido.")
                        elif scelta_profilo == '4':
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            break
                        else:
                            print("Scelta non valida, riprova.")
                elif scelta == '4':
                    break
                else:
                    print("Scelta non valida, riprova.")
            elif tipo == "artista":
                print("1: Cerca Concerto")
                print("2: Acquista Biglietti")
                print("3: Crea Concerto")
                print("4: Visualizza Situazione Biglietti")
                print("5: Duplica Concerto")
                print("6: Visualizza Utenti Biglietti")
                print("7: Profilo")
                print("8: Esci")
                scelta = input("> ")

                if scelta == '1':
                    cerca_concerto(username)
                elif scelta == '2':
                    acquista_biglietti(username)
                elif scelta == '3':
                    crea_concerto(username)
                elif scelta == '4':
                    visualizza_situazione_biglietti(username)
                elif scelta == '5':
                    duplica_concerto(username)
                elif scelta == '6':
                    visualizza_utenti_biglietti(username)
                elif scelta == '7':
                    while True:
                        print("1: Modifica Nome")
                        print("2: Modifica Password")
                        print("3: Aggiungi Saldo")
                        print("4: Visualizza Biglietti")
                        print("5: Torna al menu principale")
                        scelta_profilo = input("> ")

                        if scelta_profilo == '1':
                            nuovo_nome = input("Inserisci il nuovo nome: ")
                            modifica_nome(username, nuovo_nome)
                            username = nuovo_nome
                        elif scelta_profilo == '2':
                            vecchia_password = input("Inserisci la vecchia password: ")
                            nuova_password = input("Inserisci la nuova password: ")
                            conferma_password = input("Conferma la nuova password: ")
                            modifica_password(username, vecchia_password, nuova_password, conferma_password)
                        elif scelta_profilo == '3':
                            try:
                                importo = int(input("Inserisci l'importo da aggiungere: "))
                                aggiungi_saldo(username, importo)
                            except ValueError:
                                print("Inserisci un valore numerico valido.")
                        elif scelta_profilo == '4':
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            break
                        else:
                            print("Scelta non valida, riprova.")
                elif scelta == '8':
                    break
                else:
                    print("Scelta non valida, riprova.")

if __name__ == "__main__":
    main()
