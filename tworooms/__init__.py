from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://tr_mongo/tr_db"

from tworooms import api_routes, db