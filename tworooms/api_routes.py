from flask import request

from tworooms import app, db, gamelogic


@app.route('/')
def index():
    return "hello world!"

@app.route('/api/game', methods=['POST'])
def create_game():
    """
    receive a POST request containing the first player's name and return a new game
    """   
    if request.method == 'POST':
        mod_name = request.form['player_name']
        new_game = gamelogic.create_game(mod_name)
        db.games.insert_one(new_game)
        del new_game["_id"]
        return new_game


@app.route('/api/game/<access_code>')
def get_game(access_code):
    game = db.games.find_one_or_404({"access_code": access_code})
    del game["_id"]
    return game