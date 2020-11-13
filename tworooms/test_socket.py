import unittest

from app import app, socketio, db
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


if __name__ == "__main__":
    unittest.main()
