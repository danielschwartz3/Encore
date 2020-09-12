from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from flask import Flask
from flask import Blueprint
from server.models.genres import genre_page
from server.models.feed import feed_page

app = Flask(__name__)

app.register_blueprint(genre_page)
app.register_blueprint(feed_page)
# Use a service account

@app.route("/")
def main():
    return "Welcome to encore"