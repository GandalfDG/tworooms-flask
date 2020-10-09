import random

def generate_access_code():
    code = ''
    possible = 'abcdefghjkmnpqrstuvwxyz23456789'

    for _ in range(0, 6):
        code += random.choice(possible)

    return code.upper()


class Game():

    def create(self, mod_name):
        mod_player = Player(mod_name, True)
        game = {
            "access_code":  generate_access_code(),
            "state":        "waiting_for_players",
            "rounds":       3,
            "curr_round":   1,
            "start_time":   None,
            "players": [mod_player]
        }
        return game


class Player():

    def __init__(self, name, is_mod):
        self.name = name
        self.is_mod = False
        self.card = None

    def join_game(self, access_code):
        pass