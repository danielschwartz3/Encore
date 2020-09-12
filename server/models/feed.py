from server.firestoreWrapper import Collections
from flask import Blueprint

feed_page = Blueprint('feed_page', __name__)

class Feed:
    

    def __init__(self, user):
        self.user = user

    
    def feed_generator():
        yield ""

    @feed_page.route("/feed_next")
    def get_next_video(self):
        try:
            return next(self.feed_generator)
        except StopIteration:
            return {'id': 'end'}

