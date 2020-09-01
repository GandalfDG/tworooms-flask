from pymongo import MongoClient

client = MongoClient(host="tr_mongo", connect=True)
db = client.tr_db
games = db.games
players = db.players
