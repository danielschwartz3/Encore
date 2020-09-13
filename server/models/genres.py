from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint


genre_page = Blueprint('genre_page', __name__)


@genre_page.route("/api/genres")
def get_all_genres():
    docs = FirestoreCollections.genres_ref().stream()
    return {'genres': [doc.id for doc in docs]}
