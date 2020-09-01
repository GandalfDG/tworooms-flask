import random
from db import games, players

def generate_access_code():
    code = ''
    possible = 'abcdefghjkmnpqrstuvwxyz23456789'

    for _ in range(0, 6):
        code += random.choice(possible)

    return code.upper()

class Game():

    def create(self):
        game = {
            "access_code":  generate_access_code(),
            "state":        "waiting_for_players",
            "rounds":       3,
            "curr_round":   1,
            "start_time":   None
        }
        return games.insert_one(game)

    def read(self, access_code):
        return games.find_one({"access_code": access_code})

    def update(self, game):
        return games.replace_one({"access_code": game["access_code"]}, game, upsert=True)


    


class Player():

    def __init__(self, name):
        self.name = name
        self.is_mod = False
        self.game = None
        self.card = None

    def join_game(self, access_code):
        pass