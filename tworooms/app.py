from flask import Flask
from flask_socketio import SocketIO, send, join_room
import gamelogic as gl
from db import db, init_db_indices

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
socketio = SocketIO(app)

init_db_indices()

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
    
    # generate an access code for the game
    access_code = gl.generate_access_code()

    # create a game with the player and access code
    game = gl.create_game(access_code, player)
    db.games.insert_one(game)
    
    # send the room access code back to the creator
    send(access_code)
    join_room(access_code)

@socketio.on('join_game')
def join_game(access_code, player_name):
    """
    Find a game with the access code, and add the player to it
    """

    # find the game or error
    game = db.games.find_one({'access_code': access_code})
    if game is None:
        send("game not found")
        return

    # create a player
    player = gl.create_player(player_name)

    # add to the list of players
    db.games.update_one({'access_code': access_code}, {'$push': {'players':player}})
    
    join_room(access_code)


if __name__ == '__main__':
    socketio.run(app)