from flask import Flask
from flask_socketio import SocketIO, send, join_room
from pymongo import MongoClient
import gamelogic as gl
import db as db_utils

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
socketio = SocketIO(app)
db_client = MongoClient('mongo')
db = db_client['tworooms_db']

db_utils.init_db_indices(db)

@app.route('/')
def index():
    return 'Hello, World!'

@socketio.on('create_game')
def create_game(player_name):
    """
    Generate a room access code and create a game with the creator as the first player
    """

    # create a player with player_name who is the moderator
    player = gl.create_player(player_name, True)
    player_id = db.players.insert_one(player).inserted_id
    
    # generate an access code for the game
    access_code = gl.generate_access_code()

    # create a game with the player and access code
    game = gl.create_game(access_code, player_id)
    db.games.insert_one(game)
    
    # send the room access code back to the creator
    send(access_code)
    join_room(access_code)

if __name__ == '__main__':
    socketio.run(app)