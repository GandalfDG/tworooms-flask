import unittest

from app import app, socketio, db
import db as db_util
import gamelogic as gl
from flask_socketio import SocketIOTestClient
import random


class RoomTests(unittest.TestCase):

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

    def test_join_closed_lobby(self):
        self.client1.emit("create_game", "player1")
        access_code = self.client1.get_received()[0]['args']
        self.client1.emit('close_lobby', access_code)
        self.client2.emit("join_game", access_code, "player2")
        response = self.client2.get_received()[0]['args']
        self.assertEqual(response, 'game is in progress')
        self.assertNotIn('player2', db_util.get_players_in_lobby(access_code))


class GamePlayTests(unittest.TestCase):

    def setUp(self):
        self.clients = []
        for i in range(6):
            self.clients.append(SocketIOTestClient(app, socketio))

        self.clients[0].emit('create_game', 'player1')
        self.access_code = self.clients[0].get_received()[0]['args']
        for i in range(1, 6):
            self.clients[i].emit('join_game', self.access_code, f'player{i}')

        self.clients[0].emit('close_lobby', self.access_code)

    def testStartRound(self):
        self.clients[0].emit('start_round', self.access_code)
        received = self.clients[0].get_received()
        game = received[-1]['args'][0]
        self.assertIsNotNone(game['start_time'])


class GameLogicTest(unittest.TestCase):

    def test_shuffle_rooms(self):
        players = 7
        rooms = gl.get_shuffled_rooms(players, 123)
        self.assertTrue(len(rooms) == players)

    def test_shuffle_card_indices(self):
        players = 7
        indices = gl.get_shuffled_card_indices(players, 123)
        self.assertTrue(len(indices) == players)
        self.assertNotIn(7, indices)
        self.assertIn(6, indices)
        self.assertIn(0, indices)


if __name__ == "__main__":
    unittest.main()
