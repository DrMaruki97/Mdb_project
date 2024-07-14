import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def get_db():
    uri = "mongodb+srv://lucagiovagnoli:t7g%5EFyi7zpN!Liw@ufs13.dsmvdrx.mongodb.net/"

    client = MongoClient(uri, server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
    return client["concerti_biglietti"]
