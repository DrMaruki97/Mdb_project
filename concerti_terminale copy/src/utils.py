import pymongo

def get_db():
    uri = "mongodb+srv://fumaghe:1909,Andre@databasetox.y1r1afj.mongodb.net/"
    client = pymongo.MongoClient(uri)
    return client["concerti_biglietti"]
