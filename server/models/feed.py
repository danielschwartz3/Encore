from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint

feed_page = Blueprint('feed_page', __name__)

def feed_generator(user_id):
    user = FirestoreCollections.users_ref().document(user_id)
    reccomended_performances = FirestoreCollections.performances_ref().where(u'genres', u'array_contains_any', user.data['genres'])
    if not reccomended_performances:
        reccomended_performances = FirestoreCollections.performances_ref.stream()
    
    for performance in reccomended_performances:
        yield performance.to_dict()

@feed_page.route("/feed/<user_id>/next/", method=['GET'])
def get_next_video(user_id):
    try:
        return next(feed_generator(user_id))
    except StopIteration:
        return {'id': 'end'}
