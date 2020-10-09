import os

from flask import Flask, request
from flask_pymongo import PyMongo

from flaskr.gamelogic import Game


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        MONGO_URI = 'mongodb://tr_mongo/tr_db',
    )
    mongo = PyMongo(app)
    game_model = Game()

    @app.route('/api/game', methods=['POST'])
    def create_game():
        """
        receive a POST request containing the first player's name and return a new game
        """   
        if request.method == 'POST':
            mod_name = request.form['player_name']
            new_game = game_model.create(mod_name)
            mongo.db.games.insert_one(new_game)
            del new_game["_id"]
            return new_game


    @app.route('/api/game/<access_code>')
    def get_game(access_code):
        game = mongo.db.games.find_one_or_404({"access_code": access_code})
        del game["_id"]
        return game


    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
