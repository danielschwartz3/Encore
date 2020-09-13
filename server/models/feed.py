from login_required import login_required
from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint

feed_page = Blueprint('feed_page', __name__)


def user_feed_generator(user_id):
    user = FirestoreCollections.users_ref().document(user_id)
    reccomended_performances = FirestoreCollections.performances_ref().where(
        u'genres', u'array_contains_any', user.data['genres'])
    if not reccomended_performances:
        reccomended_performances = FirestoreCollections.performances_ref.stream()

    for performance in reccomended_performances:
        yield performance.to_dict()


def feed_generator():
    reccomended_performances = FirestoreCollections.performances_ref.stream()
    for performance in reccomended_performances:
        yield performance.to_dict()


@login_required
@feed_page.route("/api/feed/<user_id>/next/", methods=['GET'])
def get_next_user_video(user_id):
    try:
        return next(user_feed_generator(user_id))
    except StopIteration:
        return {'id': 'end'}


@feed_page.route("/api/feed/next/", methods=['GET'])
def get_next_video():
    try:
        return next(feed_generator())
    except StopIteration:
        return {'id': 'end'}
