from server.firestoreWrapper import Collections
from flask import Blueprint


genre_page = Blueprint('genre_page', __name__)


@genre_page.route("/genres")
def get_genres():
    docs = Collections.genres_ref().stream()
    return {'genres': [doc.id for doc in docs]}
