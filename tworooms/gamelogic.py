import random


def generate_access_code():
    code = ''
    possible = 'abcdefghjkmnpqrstuvwxyz23456789'

    for _ in range(0, 6):
        code += random.choice(possible)

    return code.upper()


def create_game(mod_name):
    mod_player = create_player(mod_name, True)
    game = {
        "access_code":  generate_access_code(),
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
        "card": None
    }
    return player
