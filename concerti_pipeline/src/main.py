import os
import pymongo
import bcrypt
from rich.console import Console
from rich.panel import Panel
from auth import registra_utente, login_utente, get_db 
from search import cerca_concerto
from purchase import acquista_biglietti
from profile import modifica_nome, modifica_password, aggiungi_saldo, visualizza_biglietti, visualizza_saldo, rimuovi_saldo
from artist import crea_concerto, visualizza_situazione_biglietti, duplica_concerto, visualizza_utenti_biglietti

console = Console()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    username = None
    tipo = None
    
    while True:
        clear_terminal()
        if not username:
            console.print(Panel("Benvenuto!", title="Menu Principale", style="bold blue"))
            console.print("1: Registrati")
            console.print("2: Login")
            console.print("3: Esci")
            scelta = input("> ")

            if scelta == '1':
                clear_terminal()
                username = input("Inserisci username: ")
                password = input("Inserisci password: ")
                conferma_password = input("Conferma password: ")
                tipo = input("Tipo di profilo (utente/artista): ")
                if registra_utente(username, password, conferma_password, tipo):
                    console.print("Registrazione avvenuta con successo!")
                else:
                    username = None
                input("Premi Invio per continuare...")
            elif scelta == '2':
                clear_terminal()
                username = input("Inserisci username: ")
                password = input("Inserisci password: ")
                if login_utente(username, password):
                    db = get_db()
                    user_data = db.utenti.find_one({"username": username})
                    tipo = user_data.get("tipo", "utente")
                    console.print("Login effettuato con successo!")
                else:
                    username = None
                input("Premi Invio per continuare...")
            elif scelta == '3':
                break
            else:
                console.print("[red]Scelta non valida, riprova.[/red]")
                input("Premi Invio per continuare...")
        else:
            clear_terminal()
            if tipo == "utente":
                console.print(Panel("Menu Utente", style="bold blue"))
                console.print("1: Cerca Concerto")
                console.print("2: Acquista Biglietti")
                console.print("3: Profilo")
                console.print("4: Visualizza Saldo")
                console.print("5: Logout")
                scelta = input("> ")

                if scelta == '1':
                    clear_terminal()
                    cerca_concerto(username)
                    input("Premi Invio per continuare...")
                elif scelta == '2':
                    clear_terminal()
                    acquista_biglietti(username)
                    input("Premi Invio per continuare...")
                elif scelta == '3':
                    clear_terminal()
                    while True:
                        console.print(Panel("Menu Profilo", style="bold blue"))
                        console.print("1: Modifica Nome")
                        console.print("2: Modifica Password")
                        console.print("3: Aggiungi Saldo")
                        console.print("4: Visualizza Biglietti")
                        console.print("5: Torna al menu principale")
                        scelta_profilo = input("> ")

                        if scelta_profilo == '1':
                            clear_terminal()
                            nuovo_nome = input("Inserisci il nuovo nome: ")
                            modifica_nome(username, nuovo_nome)
                            username = nuovo_nome
                        elif scelta_profilo == '2':
                            clear_terminal()
                            vecchia_password = input("Inserisci la vecchia password: ")
                            nuova_password = input("Inserisci la nuova password: ")
                            conferma_password = input("Conferma la nuova password: ")
                            modifica_password(username, vecchia_password, nuova_password, conferma_password)
                        elif scelta_profilo == '3':
                            clear_terminal()
                            try:
                                importo = int(input("Inserisci l'importo da aggiungere: "))
                                aggiungi_saldo(username, importo)
                            except ValueError:
                                console.print("[red]Inserisci un valore numerico valido.[/red]")
                        elif scelta_profilo == '4':
                            clear_terminal()
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            clear_terminal()
                            break
                        else:
                            console.print("[red]Scelta non valida, riprova.[/red]")
                        input("Premi Invio per continuare...")
                elif scelta == '4':
                    clear_terminal()
                    visualizza_saldo(username)
                    input("Premi Invio per continuare...")
                elif scelta == '5':
                    username = None
                    tipo = None
                else:
                    console.print("[red]Scelta non valida, riprova.[/red]")
                    input("Premi Invio per continuare...")
            elif tipo == "artista":
                console.print(Panel("Menu Artista", style="bold blue"))
                console.print("1: Cerca Concerto")
                console.print("2: Acquista Biglietti")
                console.print("3: Crea Concerto")
                console.print("4: Visualizza Situazione Biglietti")
                console.print("5: Duplica Concerto")
                console.print("6: Visualizza Utenti Biglietti")
                console.print("7: Profilo")
                console.print("8: Visualizza Saldo")
                console.print("9: Logout")
                scelta = input("> ")

                if scelta == '1':
                    clear_terminal()
                    cerca_concerto(username)
                    input("Premi Invio per continuare...")
                elif scelta == '2':
                    clear_terminal()
                    acquista_biglietti(username)
                    input("Premi Invio per continuare...")
                elif scelta == '3':
                    clear_terminal()
                    crea_concerto(username)
                    input("Premi Invio per continuare...")
                elif scelta == '4':
                    clear_terminal()
                    visualizza_situazione_biglietti(username)
                    input("Premi Invio per continuare...")
                elif scelta == '5':
                    clear_terminal()
                    duplica_concerto(username)
                    input("Premi Invio per continuare...")
                elif scelta == '6':
                    clear_terminal()
                    visualizza_utenti_biglietti(username)
                    input("Premi Invio per continuare...")
                elif scelta == '7':
                    clear_terminal()
                    while True:
                        console.print(Panel("Menu Profilo", style="bold blue"))
                        console.print("1: Modifica Nome")
                        console.print("2: Modifica Password")
                        console.print("3: Aggiungi Saldo")
                        console.print("4: Visualizza Biglietti")
                        console.print("5: Torna al menu principale")
                        scelta_profilo = input("> ")

                        if scelta_profilo == '1':
                            clear_terminal()
                            nuovo_nome = input("Inserisci il nuovo nome: ")
                            modifica_nome(username, nuovo_nome)
                            username = nuovo_nome
                        elif scelta_profilo == '2':
                            clear_terminal()
                            vecchia_password = input("Inserisci la vecchia password: ")
                            nuova_password = input("Inserisci la nuova password: ")
                            conferma_password = input("Conferma la nuova password: ")
                            modifica_password(username, vecchia_password, nuova_password, conferma_password)
                        elif scelta_profilo == '3':
                            clear_terminal()
                            try:
                                importo = int(input("Inserisci l'importo da aggiungere: "))
                                aggiungi_saldo(username, importo)
                            except ValueError:
                                console.print("[red]Inserisci un valore numerico valido.[/red]")
                        elif scelta_profilo == '4':
                            clear_terminal()
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            clear_terminal()
                            break
                        else:
                            console.print("[red]Scelta non valida, riprova.[/red]")
                        input("Premi Invio per continuare...")
                elif scelta == '8':
                    clear_terminal()
                    visualizza_saldo(username)
                    input("Premi Invio per continuare...")
                elif scelta == '9':
                    username = None
                    tipo = None
                else:
                    console.print("[red]Scelta non valida, riprova.[/red]")
                    input("Premi Invio per continuare...")

if __name__ == "__main__":
    main()
