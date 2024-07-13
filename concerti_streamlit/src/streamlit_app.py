import streamlit as st
from pymongo import MongoClient
import bcrypt
from geopy.geocoders import Nominatim
import uuid
from datetime import datetime

# Funzioni di utilità
def get_db():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = MongoClient(uri)
    return client["concerti_biglietti"]

def login(username, password):
    db = get_db()
    user = db.utenti.find_one({"username": username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return user
    return None

def registra(username, password, tipo):
    db = get_db()
    if db.utenti.find_one({"username": username}):
        return False
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.utenti.insert_one({"username": username, "password": hashed, "tipo": tipo, "saldo": 0, "biglietti": []})
    if tipo == "artista":
        artista = db.artisti.find_one({"nome": username})
        if artista:
            db.artisti.update_one({"_id": artista["_id"]}, {"$set": {"utente": username}})
        else:
            db.artisti.insert_one({"nome": username, "utente": username})
    return True

def cerca_concerto_per_artista(username):
    db = get_db()
    artisti = list(db.artisti.find({}))
    artista_scelto = st.selectbox("Seleziona un artista", artisti, format_func=lambda artista: artista['nome'])
    if artista_scelto:
        concerti = list(db.concerti.find({"artista_id": artista_scelto["_id"]}))
        for concerto in concerti:
            st.write(f"{concerto['nome']}, {concerto['data']}, Artista: {concerto['artista_id']}, Location: {concerto['location_id']}")
            for settore in concerto['settori']:
                st.write(f"    Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

def cerca_concerto_per_date(username):
    db = get_db()
    data_inizio = st.date_input("Data inizio")
    data_fine = st.date_input("Data fine")
    if st.button("Cerca"):
        concerti = list(db.concerti.find({"data": {"$gte": str(data_inizio), "$lte": str(data_fine)}}))
        for concerto in concerti:
            st.write(f"{concerto['nome']}, {concerto['data']}, Artista: {concerto['artista_id']}, Location: {concerto['location_id']}")
            for settore in concerto['settori']:
                st.write(f"    Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

def cerca_concerto_per_vicinanza(username):
    db = get_db()
    indirizzo = st.text_input("Inserisci l'indirizzo")
    geolocator = Nominatim(user_agent="vicinanza_concerto")
    location = geolocator.geocode(indirizzo)
    if location:
        raggio = st.number_input("Raggio in km", min_value=1, max_value=1000, step=1)
        if st.button("Cerca"):
            concerti = list(db.concerti.aggregate([
                {
                    '$geoNear': {
                        'near': {
                            'type': 'Point',
                            'coordinates': [location.longitude, location.latitude]
                        },
                        'distanceField': 'distance',
                        'maxDistance': raggio * 1000,
                        'spherical': True
                    }
                }
            ]))
            for concerto in concerti:
                st.write(f"{concerto['nome']}, {concerto['data']}, Artista: {concerto['artista_id']}, Location: {concerto['location_id']}")
                for settore in concerto['settori']:
                    st.write(f"    Settore: {settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")

def acquista_biglietti(username):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    
    concerti = list(db.concerti.find({}))
    if not concerti:
        st.write("Nessun concerto disponibile per l'acquisto.")
        return

    concerto_scelto = st.selectbox("Seleziona un concerto", concerti, format_func=lambda concerto: f"{concerto['nome']}, {concerto['data']}")
    
    if concerto_scelto:
        settore_scelto = st.selectbox("Seleziona un settore", concerto_scelto['settori'], format_func=lambda settore: f"{settore['nome']}, Prezzo: {settore['prezzo']}€, Posti disponibili: {settore['posti_disponibili']}")
        quantita = st.number_input("Quanti biglietti?", min_value=1, max_value=settore_scelto['posti_disponibili'], step=1)

        if st.button("Acquista"):
            if utente["saldo"] < settore_scelto['prezzo'] * quantita:
                st.write("Saldo insufficiente per completare l'acquisto.")
                return
            settore_scelto['posti_disponibili'] -= quantita
            biglietto = {
                "id": str(uuid.uuid4()),
                "concerto": concerto_scelto['nome'],
                "data": concerto_scelto['data'],
                "settore": settore_scelto['nome'],
                "prezzo": settore_scelto['prezzo'],
                "quantita": quantita
            }
            db.utenti.update_one(
                {"username": username},
                {"$push": {"biglietti": biglietto}}
            )
            db.concerti.update_one(
                {"_id": concerto_scelto["_id"], "settori.nome": settore_scelto['nome']},
                {"$set": {"settori.$.posti_disponibili": settore_scelto['posti_disponibili']}}
            )
            st.write(f"I tuoi biglietti per un totale di {settore_scelto['prezzo'] * quantita}€:")
            st.write(f"Codice: {biglietto['id']}, {biglietto['concerto']}, {biglietto['data']}, Settore: {biglietto['settore']}, Prezzo: {biglietto['prezzo']}€, Quantità: {biglietto['quantita']}")
            st.write(f"Saldo rimanente: {utente['saldo'] - settore_scelto['prezzo'] * quantita}€")
            db.utenti.update_one(
                {"username": username},
                {"$inc": {"saldo": -settore_scelto['prezzo'] * quantita}}
            )

def crea_concerto(username):
    db = get_db()
    geolocator = Nominatim(user_agent="concert_creator")

    nome_concerto = st.text_input("Nome del concerto")
    data = st.date_input("Data del concerto")
    location_nome = st.text_input("Nome della location")

    if st.button("Crea Concerto"):
        location = db.location.find_one({"nome": location_nome})
        
        if location:
            location_id = location["_id"]
        else:
            location_geocode = geolocator.geocode(location_nome)
            if not location_geocode:
                st.write(f"Impossibile trovare le coordinate per {location_nome}")
                return
            
            location_id = f"{location_nome.replace(' ', '_')}_{location_geocode.latitude}_{location_geocode.longitude}"
            location_doc = {
                "_id": location_id,
                "nome": location_nome,
                "coordinate": {
                    "type": "Point",
                    "coordinates": [location_geocode.longitude, location_geocode.latitude]
                },
                "indirizzo": location_geocode.address
            }
            db.location.insert_one(location_doc)

        settori = []
        n_settori = st.number_input("Numero di settori", min_value=1, step=1)
        for _ in range(n_settori):
            settore_nome = st.text_input("Nome del settore")
            prezzo = st.number_input("Prezzo del settore", min_value=0.0, step=0.01)
            posti_disponibili = st.number_input("Posti disponibili", min_value=1, step=1)
            settori.append({
                "nome": settore_nome,
                "prezzo": prezzo,
                "posti_disponibili": posti_disponibili
            })

        artista_doc = db.artisti.find_one({"nome": username})
        if not artista_doc:
            st.write("Errore: Artista non trovato.")
            return

        artista_id = artista_doc["_id"]

        concerto = {
            "nome": nome_concerto,
            "data": str(data),
            "artista_id": artista_id,
            "location_id": location_id,
            "settori": settori
        }

        db.concerti.insert_one(concerto)
        st.write("Concerto creato con successo!")

def visualizza_situazione_biglietti(username):
    db = get_db()
    artista_doc = db.artisti.find_one({"nome": username})
    if not artista_doc:
        st.write("Nessun artista trovato con questo nome.")
        return
    
    artista_id = artista_doc["_id"]
    concerti = list(db.concerti.find({"artista_id": artista_id}))
    
    if len(concerti) == 0:
        st.write("Nessun concerto trovato per l'artista.")
        return
    
    for concerto in concerti:
        st.write(f"Concerto: {concerto['nome']}, Data: {concerto['data']}")
        for settore in concerto['settori']:
            st.write(f"    Settore: {settore['nome']}, Posti rimanenti: {settore['posti_disponibili']}")
            
def duplica_concerto(username):
    db = get_db()
    artista_doc = db.artisti.find_one({"nome": username})
    if not artista_doc:
        st.write("Nessun artista trovato con questo nome.")
        return
    
    artista_id = artista_doc["_id"]
    concerti = list(db.concerti.find({"artista_id": artista_id}))
    
    if not concerti:
        st.write("Nessun concerto trovato per l'artista.")
        return
    
    concerto_scelto = st.selectbox("Seleziona un concerto da duplicare", concerti, format_func=lambda concerto: f"{concerto['nome']}, {concerto['data']}")
    nuova_data = st.date_input("Inserisci la nuova data")

    if st.button("Duplica Concerto"):
        nuovo_concerto = concerto_scelto.copy()
        nuovo_concerto['_id'] = str(uuid.uuid4())
        nuovo_concerto['data'] = str(nuova_data)
        
        db.concerti.insert_one(nuovo_concerto)
        st.write("Concerto duplicato con successo!")

def visualizza_utenti_biglietti(username):
    db = get_db()
    artista_doc = db.artisti.find_one({"nome": username})
    if not artista_doc:
        st.write("Nessun artista trovato con questo nome.")
        return
    
    artista_id = artista_doc["_id"]
    concerti = list(db.concerti.find({"artista_id": artista_id}))
    
    if len(concerti) == 0:
        st.write("Nessun concerto trovato per l'artista.")
        return
    
    for concerto in concerti:
        st.write(f"Concerto: {concerto['nome']}, Data: {concerto['data']}")
        utenti = list(db.utenti.find({"biglietti.concerto": concerto['nome']}))
        if len(utenti) == 0:
            st.write("Nessun utente ha acquistato i biglietti per questo concerto.")
            continue
        for utente in utenti:
            biglietti_utente = [biglietto for biglietto in utente['biglietti'] if biglietto['concerto'] == concerto['nome']]
            for biglietto in biglietti_utente:
                st.write(f"    Utente: {utente['username']}, Settore: {biglietto['settore']}, Quantità: {biglietto['quantita']}")

def profilo(username):
    db = get_db()
    utente = db.utenti.find_one({"username": username})
    st.write(f"Nome utente: {utente['username']}")
    st.write(f"Saldo: {utente['saldo']}€")

    nuova_password = st.text_input("Nuova Password", type="password")
    conferma_password = st.text_input("Conferma Nuova Password", type="password")
    if st.button("Aggiorna Password"):
        if nuova_password == conferma_password:
            hashed = bcrypt.hashpw(nuova_password.encode('utf-8'), bcrypt.gensalt())
            db.utenti.update_one({"username": username}, {"$set": {"password": hashed}})
            st.write("Password aggiornata con successo!")
        else:
            st.write("Le password non corrispondono.")

    nuovo_nome = st.text_input("Nuovo Nome Utente")
    if st.button("Aggiorna Nome Utente"):
        if nuovo_nome:
            db.utenti.update_one({"username": username}, {"$set": {"username": nuovo_nome}})
            st.session_state["username"] = nuovo_nome
            st.write("Nome utente aggiornato con successo!")

    aggiungi_saldo = st.number_input("Aggiungi Saldo", min_value=1, step=1)
    if st.button("Aggiungi"):
        db.utenti.update_one({"username": username}, {"$inc": {"saldo": aggiungi_saldo}})
        st.write(f"{aggiungi_saldo}€ aggiunti al saldo!")

    st.write("Biglietti acquistati:")
    biglietti = utente.get("biglietti", [])
    if biglietti:
        concerti_acquistati = set(biglietto["concerto"] for biglietto in biglietti)
        concerto_scelto = st.selectbox("Seleziona un concerto", list(concerti_acquistati))
        biglietti_concerto = [biglietto for biglietto in biglietti if biglietto["concerto"] == concerto_scelto]
        for biglietto in biglietti_concerto:
            st.write(f"Codice: {biglietto['id']}, Data: {biglietto['data']}, Settore: {biglietto['settore']}, Prezzo: {biglietto['prezzo']}€, Quantità: {biglietto['quantita']}")
    else:
        st.write("Non hai biglietti acquistati.")

# Interfaccia Streamlit
st.title("Gestione Concerti")

if "username" not in st.session_state:
    st.session_state["username"] = None

if st.session_state["username"]:
    db = get_db()
    user = db.utenti.find_one({"username": st.session_state["username"]})
    st.sidebar.write(f"Benvenuto, {st.session_state['username']}!")
    
    if user["tipo"] == "artista":
        page = st.sidebar.selectbox("Seleziona una pagina", ["Cerca Concerto", "Acquista Biglietti", "Crea Concerto", "Visualizza Situazione Biglietti", "Duplica Concerto", "Visualizza Utenti Biglietti", "Profilo", "Logout"])
    else:
        page = st.sidebar.selectbox("Seleziona una pagina", ["Cerca Concerto", "Acquista Biglietti", "Profilo", "Logout"])

    if page == "Cerca Concerto":
        search_type = st.selectbox("Tipo di ricerca", ["Per Artista", "Per Date", "Per Vicinanza"])
        if search_type == "Per Artista":
            cerca_concerto_per_artista(st.session_state["username"])
        elif search_type == "Per Date":
            cerca_concerto_per_date(st.session_state["username"])
        elif search_type == "Per Vicinanza":
            cerca_concerto_per_vicinanza(st.session_state["username"])
    elif page == "Acquista Biglietti":
        acquista_biglietti(st.session_state["username"])
    elif page == "Crea Concerto" and user["tipo"] == "artista":
        crea_concerto(st.session_state["username"])
    elif page == "Visualizza Situazione Biglietti" and user["tipo"] == "artista":
        visualizza_situazione_biglietti(st.session_state["username"])
    elif page == "Duplica Concerto" and user["tipo"] == "artista":
        duplica_concerto(st.session_state["username"])
    elif page == "Visualizza Utenti Biglietti" and user["tipo"] == "artista":
        visualizza_utenti_biglietti(st.session_state["username"])
    elif page == "Profilo":
        profilo(st.session_state["username"])
    elif page == "Logout":
        st.session_state["username"] = None
        st.rerun()
else:
    st.sidebar.write("Accedi o Registrati")
    page = st.sidebar.selectbox("Seleziona una pagina", ["Login", "Registrati"])

    if page == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state["username"] = user["username"]
                st.rerun()
            else:
                st.write("Username o password errati")

    elif page == "Registrati":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        conferma_password = st.text_input("Conferma Password", type="password")
        tipo = st.selectbox("Tipo di profilo", ["utente", "artista"])
        if st.button("Registrati"):
            if password == conferma_password:
                success = registra(username, password, tipo)
                if success:
                    st.write("Registrazione avvenuta con successo!")
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.write("Errore nella registrazione. Username potrebbe essere già in uso.")
            else:
                st.write("Le password non corrispondono.")
