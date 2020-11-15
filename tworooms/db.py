from pymongo import MongoClient

db = MongoClient('mongo')['tworooms_db']


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


def create_game(access_code, mod_player):
    game = {
        "access_code":  access_code,
        "state":        "waiting_for_players",
        "rounds":       3,
        "curr_round":   1,
        "start_time":   None,
        "players": [mod_player]
    }
    return game


def create_player(name, is_mod=False):
    player = {
        "name": name,
        "is_mod": is_mod,
        "start_room": None,
        "card": None
    }
    return player
