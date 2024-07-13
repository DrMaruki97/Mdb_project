from search import cerca_concerto
from purchase import acquista_biglietti

def main():
    while True:
        print("1: Cerca Concerto")
        print("2: Acquista Biglietti")
        print("3: Esci")
        scelta = input("> ")

        if scelta == '1':
            cerca_concerto()
        elif scelta == '2':
            acquista_biglietti()
        elif scelta == '3':
            break
        else:
            print("Scelta non valida, riprova.")

if __name__ == "__main__":
    main()
