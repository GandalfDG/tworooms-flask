import unittest

from app import app, socketio, db
from flask_socketio import SocketIOTestClient


class SocketTest(unittest.TestCase):
    
    def setUp(self):
        self.client = SocketIOTestClient(app, socketio)
    
    def test_create_game(self):
        self.client.emit("create_game", "player1")
        access_code = self.client.get_received()[0]['args']
        self.assertIsNotNone(access_code)
        self.assertIsNotNone(db.games.find_one({"access_code": access_code}))

if __name__ == "__main__":
    unittest.main()
