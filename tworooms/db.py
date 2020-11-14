from pymongo import MongoClient

db_client = MongoClient('mongo')
db = db_client['tworooms_db']

def init_db_indices():
    db.games.create_index("access_code")

def get_players_in_lobby(access_code: str) -> list:
    players = []
    player_ids = db.games.find_one({'access_code': access_code})['players']
    for id in player_ids:
        players.append(db.players.find_one({'_id': id})['name'])

    return players
