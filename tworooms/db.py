from pymongo import MongoClient

db_client = MongoClient('mongo')
db = db_client['tworooms_db']


def init_db_indices():
    db.games.create_index("access_code")


def get_game(access_code):
    return db.games.find_one({'access_code': access_code})


def get_players_in_lobby(access_code: str) -> list:
    player_names = []
    players = get_game(access_code)['players']
    for player in players:
        player_names.append(player.get('name'))

    return player_names
