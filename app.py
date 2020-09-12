from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from flask import Flask
<<<<<<< Updated upstream


app = Flask(__name__)


=======
from flask import Blueprint
from server.models.genres import genre_page
from server.models.users import user_page

app = Flask(__name__)

app.register_blueprint(genre_page)
app.register_blueprint(user_page)
>>>>>>> Stashed changes
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