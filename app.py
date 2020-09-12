import firebase_admin
from firebase_admin import credentials, firestore
from flask import Blueprint, Flask, request, session

from server.models.chat_rooms import chat_room_page
from server.models.feed import feed_page
from server.models.genres import genre_page
from server.models.performances import performance_page
from server.models.scheduled_performances import scheduled_performance_page
from server.models.users import user_page


app = Flask(__name__)


app.secret_key = "^d*ÎˇÁÔÒÔ˝◊ÇÎNJGHCFDDRT^YUOIÔ˝ÇÎ˛›ﬁﬂ‡°·‚·ﬁ›‹›ﬁﬂ‡°·°‡ﬂﬁ›‹›ﬁﬂ‡°·°‡ﬂﬁ›‹FGHNBVCXSRJTGVM"


app.register_blueprint(genre_page)
app.register_blueprint(feed_page)
app.register_blueprint(user_page)
app.register_blueprint(chat_room_page)
app.register_blueprint(performance_page)
app.register_blueprint(scheduled_performance_page)
# Use a service account



@app.route("/")
def main():
    return "Welcome to encore"
