from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room
import gamelogic as gl
import db as db_util
from db import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secret'
socketio = SocketIO(app)

db_util.init_db_indices()


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
    while True:
        access_code = gl.generate_access_code()
        if db.games.count_documents({'access_code': access_code}) == 0:
            break

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
    game = db_util.get_game(access_code)
    if game is None:
        send('game not found')
        return

    if game['state'] != 'waiting_for_players':
        send('game is in progress')
        return

    # create a player
    player = gl.create_player(player_name)

    # add to the list of players
    db.games.update_one({'access_code': access_code}, {
                        '$push': {'players': player}})

    join_room(access_code)
    emit('lobby_update', {'players': db_util.get_players_in_lobby(
        access_code)}, room=access_code)


@socketio.on('close_lobby')
def close_lobby(access_code):
    """
    Close the lobby and direct each player to their starting room
    """
    game = db_util.get_game(access_code)
    num_players = len(game['players'])
    rooms = gl.get_shuffled_rooms(num_players)

    for room, player in zip(rooms, game['players']):
        player['start_room'] = room

    # update the players with their rooms and change the game state
    db.games.find_one_and_update({'access_code': access_code},
                                 {'$set': {'players': game['players'],
                                           'state': 'readying_rooms'}})



if __name__ == '__main__':
    socketio.run(app)
