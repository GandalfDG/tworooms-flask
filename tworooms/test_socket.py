import unittest

from app import app, socketio, db
import db as db_util
import gamelogic as gl
from flask_socketio import SocketIOTestClient


class SocketTest(unittest.TestCase):

    def setUp(self):
        self.client1 = SocketIOTestClient(app, socketio)
        self.client2 = SocketIOTestClient(app, socketio)

    def test_create_game(self):
        self.client1.emit("create_game", "player1")
        access_code = self.client1.get_received()[0]['args']
        self.assertIsNotNone(access_code)
        self.assertIsNotNone(db.games.find_one({"access_code": access_code}))

    def test_join_game(self):
        self.client1.emit("create_game", "player1")
        access_code = self.client1.get_received()[0]['args']
        self.client2.emit("join_game", access_code, "player2")
        self.assertTrue(len(db.games.find_one(
            {'access_code': access_code})['players']) == 2)

        lobby_players = db_util.get_players_in_lobby(access_code)
        self.assertIn('player1', lobby_players)
        self.assertIn('player2', lobby_players)
        self.assertNotIn('player3', lobby_players)

        received = self.client1.get_received()
        self.assertIn('player1', received[0]['args'][0]['players'])

    def test_close_lobby(self):
        self.client1.emit("create_game", "player1")
        access_code = self.client1.get_received()[0]['args']
        self.client2.emit("join_game", access_code, "player2")
        game = db_util.get_game(access_code)
        self.assertIsNone(game['players'][0]['start_room'])
        self.client1.emit('close_lobby', access_code)
        game = db_util.get_game(access_code)
        self.assertIsNotNone(game['players'][0]['start_room'])

class GameLogicTest(unittest.TestCase):

    def test_shuffle_rooms(self):
        players = 7
        rooms = gl.get_shuffled_rooms(players)
        self.assertTrue(len(rooms) == players)


if __name__ == "__main__":
    unittest.main()
