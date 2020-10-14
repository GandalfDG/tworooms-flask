from tworooms import app
from flask_pymongo import PyMongo

mongo = PyMongo(app)
games = mongo.db.games
