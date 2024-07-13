from rich.console import Console
from rich.panel import Panel  # Aggiunta importazione di Panel
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
            console.print(Panel("[bold]Benvenuto![/bold]\n1: Registrati\n2: Login", title="Menu Principale", style="cyan"))
            scelta = input("> ")

            if scelta == '1':
                username = input("Inserisci username: ")
                password = input("Inserisci password: ")
                conferma_password = input("Conferma password: ")
                tipo = input("Tipo di profilo (utente/artista): ")
                if registra_utente(username, password, conferma_password, tipo):
                    console.print("[bold green]Registrazione avvenuta con successo![/bold green]")
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
                console.print(Panel("[bold]Menu Utente[/bold]\n1: Cerca Concerto\n2: Acquista Biglietti\n3: Profilo\n4: Esci", style="cyan"))
                scelta = input("> ")

                if scelta == '1':
                    cerca_concerto(username)
                elif scelta == '2':
                    acquista_biglietti(username)
                elif scelta == '3':
                    while True:
                        console.print(Panel("[bold]Menu Profilo[/bold]\n1: Modifica Nome\n2: Modifica Password\n3: Aggiungi Saldo\n4: Visualizza Biglietti\n5: Torna al menu principale", style="cyan"))
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
                                console.print("[red]Inserisci un valore numerico valido.[/red]")
                        elif scelta_profilo == '4':
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            break
                        else:
                            console.print("[red]Scelta non valida, riprova.[/red]")
                elif scelta == '4':
                    break
                else:
                    console.print("[red]Scelta non valida, riprova.[/red]")
            elif tipo == "artista":
                console.print(Panel("[bold]Menu Artista[/bold]\n1: Cerca Concerto\n2: Acquista Biglietti\n3: Crea Concerto\n4: Visualizza Situazione Biglietti\n5: Duplica Concerto\n6: Visualizza Utenti Biglietti\n7: Profilo\n8: Esci", style="cyan"))
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
                        console.print(Panel("[bold]Menu Profilo[/bold]\n1: Modifica Nome\n2: Modifica Password\n3: Aggiungi Saldo\n4: Visualizza Biglietti\n5: Torna al menu principale", style="cyan"))
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
                                console.print("[red]Inserisci un valore numerico valido.[/red]")
                        elif scelta_profilo == '4':
                            visualizza_biglietti(username)
                        elif scelta_profilo == '5':
                            break
                        else:
                            console.print("[red]Scelta non valida, riprova.[/red]")
                elif scelta == '8':
                    break
                else:
                    console.print("[red]Scelta non valida, riprova.[/red]")

if __name__ == "__main__":
    main()
