# Sistema di Gestione di concerti

Questo progetto è un sistema di gestione dei concerti che consente agli artisti di creare, duplicare e gestire concerti, e agli utenti di cercare e acquistare biglietti. Utilizza MongoDB per l'archiviazione dei dati e fornisce un'interfaccia basata su terminale per l'interazione.

## Caratteristiche

- **Registrazione e Login Utente**: Gli utenti possono registrarsi come utenti regolari o artisti.
- **Creazione di Concerti**: Gli artisti possono creare nuovi concerti con più settori.
- **Visualizzazione Situazione Biglietti**: Gli artisti possono vedere la disponibilità dei biglietti per i loro concerti.
- **Duplicazione di Concerti**: Gli artisti possono duplicare concerti esistenti a una nuova data.
- **Visualizzazione Acquirenti Biglietti**: Gli artisti possono vedere gli utenti che hanno acquistato i biglietti per i loro concerti.
- **Ricerca e Acquisto Biglietti**: Gli utenti possono cercare concerti e acquistare biglietti.
- **Gestione Profilo**: Gli utenti possono modificare il loro profilo, aggiungere saldo e visualizzare i loro biglietti.

## Strumenti Utilizzati
**Python**: Linguaggio di programmazione principale utilizzato per sviluppare il progetto.
- *pymongo*: Libreria Python per interagire con MongoDB.
- *bcrypt*: Libreria per l'hashing delle password e la sicurezza.
- *rich*: Libreria per creare interfacce terminali colorate e interattive.
- *geopy*: Libreria per ottenere coordinate geografiche basate su indirizzi.
  
**MongoDB**: Database NoSQL utilizzato per archiviare dati degli utenti, concerti, biglietti, ecc.

## Installazione

1. **Clona il repository**:
    ```bash
    git clone https://github.com/DrMaruki97/Mdb_project.git
    cd Mdb_project/concerti_terminale
    ```

2. **Installa le dipendenze**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configura MongoDB**:
    - Assicurati che MongoDB sia in esecuzione e accessibile.
    - Aggiorna l'URI di MongoDB in `auth.py` se necessario.

4. **Carica i Dati Iniziali**:
    ```bash
    python db_setup.py
    ```

## Uso

1. **Esegui lo script principale**:
    ```bash
    python main.py
    ```

2. **Segui i prompt**:
    - Registrati o effettua il login.
    - A seconda del tipo di utente (utente regolare o artista), saranno disponibili diverse opzioni di menu.

## Panoramica dei File

- `artisti.py`: Contiene funzioni per gli artisti per gestire i concerti.
- `auth.py`: Gestisce l'autenticazione degli utenti e la connessione al database.
- `db_setup.py`: Configura il database con i dati iniziali.
- `main.py`: Lo script principale che fornisce l'interfaccia del terminale.
- `search.py`: Gestisce la ricerca dei concerti.
- `purchase.py`: Gestisce l'acquisto dei biglietti.
- `profile.py`: Gestisce le operazioni del profilo utente.

## Licenza

Questo progetto è concesso in licenza sotto la licenza MIT.

## Autori

- [DrMaruki97](https://github.com/DrMaruki97)
```
