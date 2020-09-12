from flask_login.utils import login_required
from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint


genre_page = Blueprint('genre_page', __name__)

@login_required
@genre_page.route("/genres", methods=['GET'])
def get_all_genres():
    docs = FirestoreCollections.genres_ref().stream()
    return {'genres': [doc.id for doc in docs]}
