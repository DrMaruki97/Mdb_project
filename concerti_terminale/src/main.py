from rich.console import Console
from rich.table import Table
from search import cerca_concerto, acquista_biglietti
from auth import registra_utente, login_utente
from profile import modifica_nome, modifica_password, aggiungi_saldo, visualizza_biglietti
from artist import crea_concerto, visualizza_situazione_biglietti, duplica_concerto, visualizza_utenti_biglietti
from utils import get_db

console = Console()

def main():
    username = None
    tipo = None

    while True:
        if not username:
            console.print("1: [bold]Registrati[/bold]", style="cyan")
            console.print("2: [bold]Login[/bold]", style="cyan")
            scelta = input("> ")

            if scelta == '1':
                username = input("Inserisci username: ")
                password = input("Inserisci password: ")
                conferma_password = input("Conferma password: ")
                tipo = input("Tipo di profilo (utente/artista): ")
                if registra_utente(username, password, conferma_password, tipo):
                    console.print("Registrazione avvenuta con successo!", style="green")
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
                console.print("1: [bold]Cerca Concerto[/bold]", style="cyan")
                console.print("2: [bold]Acquista Biglietti[/bold]", style="cyan")
                console.print("3: [bold]Profilo[/bold]", style="cyan")
                console.print("4: [bold]Esci[/bold]", style="cyan")
                scelta = input("> ")

                if scelta == '1':
                    cerca_concerto(username)
                elif scelta == '2':
                    acquista_biglietti(username)
                elif scelta == '3':
                    while True:
                        console.print("1: [bold]Modifica Nome[/bold]", style="cyan")
                        console.print("2: [bold]Modifica Password[/bold]", style="cyan")
                        console.print("3: [bold]Aggiungi Saldo[/bold]", style="cyan")
                        console.print("4: [bold]Visualizza Biglietti[/bold]", style="cyan")
                        console.print("5: [bold]Torna al menu principale[/bold]", style="cyan")
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
                                console.print("Inserisci un valore numerico valido.", style="red")
                        elif scelta_profilo == '4':
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            break
                        else:
                            console.print("Scelta non valida, riprova.", style="red")
                elif scelta == '4':
                    break
                else:
                    console.print("Scelta non valida, riprova.", style="red")
            elif tipo == "artista":
                console.print("1: [bold]Cerca Concerto[/bold]", style="cyan")
                console.print("2: [bold]Acquista Biglietti[/bold]", style="cyan")
                console.print("3: [bold]Crea Concerto[/bold]", style="cyan")
                console.print("4: [bold]Visualizza Situazione Biglietti[/bold]", style="cyan")
                console.print("5: [bold]Duplica Concerto[/bold]", style="cyan")
                console.print("6: [bold]Visualizza Utenti Biglietti[/bold]", style="cyan")
                console.print("7: [bold]Profilo[/bold]", style="cyan")
                console.print("8: [bold]Esci[/bold]", style="cyan")
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
                        console.print("1: [bold]Modifica Nome[/bold]", style="cyan")
                        console.print("2: [bold]Modifica Password[/bold]", style="cyan")
                        console.print("3: [bold]Aggiungi Saldo[/bold]", style="cyan")
                        console.print("4: [bold]Visualizza Biglietti[/bold]", style="cyan")
                        console.print("5: [bold]Torna al menu principale[/bold]", style="cyan")
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
                                console.print("Inserisci un valore numerico valido.", style="red")
                        elif scelta_profilo == '4':
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            break
                        else:
                            console.print("Scelta non valida, riprova.", style="red")
                elif scelta == '8':
                    break
                else:
                    console.print("Scelta non valida, riprova.", style="red")

if __name__ == "__main__":
    main()
