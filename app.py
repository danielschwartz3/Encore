from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from flask import Flask


app = Flask(__name__)


# Use a service account
cred = credentials.Certificate('encore-1e5ea-firebase-adminsdk-qrpzn-39bbdd3196.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

    
def genres_ref():
    return db.collection(u'genres')


@app.route("/genres")
def get_genres():
    docs = genres_ref().stream()
    return {'genres': [doc.id for doc in docs]}

@app.route("/")
def main():
    return "Welcome to encore"