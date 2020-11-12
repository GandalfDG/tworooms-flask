from flask import Flask
from flask_socketio import SocketIO
from pymongo import MongoClient
import gamelogic as gl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
socketio = SocketIO(app)
db_client = MongoClient('mongo')
db = db_client['tworooms_db']

@app.route('/')
def index():
    create_game("Jack")
    return 'Hello, World!'

@socketio.on('create_game')
def create_game(player_name):
    """
    Generate a room access code and create a game with the creator as the first player
    """
    player = gl.create_player(player_name, True)
    player_id = db.players.insert_one(player).inserted_id
    
    access_code = gl.generate_access_code()

    game = gl.create_game(access_code, player_id)
    db.games.insert_one

if __name__ == '__main__':
    socketio.run(app)