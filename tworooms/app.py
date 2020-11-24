from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room
import gamelogic as gl
import db as db_util
from db import db
from pymongo import ReturnDocument
from datetime import datetime

socketio = SocketIO()


def create_app(debug=false):
    app = Flask(__name__)
    app.debug = debug

    socketio.init_app(app)
    return app

@app.route('/')
def index():
    return 'Hello, World!'


@socketio.on('create_game')
def create_game(player_name):
    """
    Generate a room access code and create a game with the creator as the first player
    """

    # create a player with player_name who is the moderator
    player = db_util.create_player(player_name, True)

    # generate an access code for the game
    while True:
        access_code = gl.generate_access_code()
        if db.games.count_documents({'access_code': access_code}) == 0:
            break

    # create a game with the player and access code
    game = db_util.create_game(access_code, player)
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
    player = db_util.create_player(player_name)

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
    cards = gl.get_shuffled_card_indices(num_players)

    for room, card, player in zip(rooms, cards, game['players']):
        player['start_room'] = room
        player['card'] = card

    # update the players with their rooms and change the game state
    game = db.games.find_one_and_update({'access_code': access_code},
                                        {'$set': {'players': game['players'],
                                                  'state': 'readying_rooms'}},
                                        return_document=ReturnDocument.AFTER)

    emit('game_update', game, room=access_code)


@socketio.on('start_round')
def start_round(access_code):
    """
    Start the round timer by sending the round start time to the players in the room
    """
    start_time = datetime.now().isoformat()
    game = db.games.find_one_and_update({'access_code': access_code}, {
        '$set': {'start_time': start_time}}, return_document=ReturnDocument.AFTER)

    emit('start_round', game, room=access_code)


if __name__ == '__main__':
    socketio.run(app)
