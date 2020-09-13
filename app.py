from functools import wraps

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Blueprint, Flask, g, redirect, request, session, url_for
from flask.templating import render_template
from flask_socketio import SocketIO, join_room

from login_required import login_required
#***********
from server.firestoreWrapper import FirestoreCollections
# from server.models.chat_rooms import chat_room_page
from server.models.feed import feed_page
from server.models.genres import genre_page
from server.models.performances import performance_page
from server.models.scheduled_performances import scheduled_performance_page
from server.models.users import user_page

app = Flask(__name__)
socketio = SocketIO(app)

app.secret_key = "^d*ÎˇÁÔÒÔ˝◊ÇÎNJGHCFDDRT^YUOIÔ˝ÇÎ˛›ﬁﬂ‡°·‚·ﬁ›‹›ﬁﬂ‡°·°‡ﬂﬁ›‹›ﬁﬂ‡°·°‡ﬂﬁ›‹FGHNBVCXSRJTGVM"


app.register_blueprint(genre_page)
app.register_blueprint(feed_page)
app.register_blueprint(user_page)
# app.register_blueprint(chat_room_page)
app.register_blueprint(performance_page)
app.register_blueprint(scheduled_performance_page)
# Use a service account


@app.route("/")
def main():
    return "Welcome to encore"



# chat_room_page = Blueprint('chat_room_page', __name__)

@app.route("/chat_rooms", methods=['GET'])
def get_all_chat_rooms():
    docs = FirestoreCollections.chat_rooms_ref().stream()
    return {'chat_rooms': [doc.to_dict() for doc in docs]}


@app.route("/chat_home")
def chat_home():
    return render_template('index.html')


@app.route("/chat")
def chat():
    user_name = request.args.get('user_name')
    chat_room_id = request.args.get('chat_room_id')
    if user_name and chat_room_id:
        return render_template('chat.html', user_name = user_name, chat_room_id = chat_room_id)
    else:
        return redirect(url_for('chat_home'))

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the chat".format(data['user_name']))
    join_room(data['chat_room_id'])
    socketio.emit('join_room_announcement', data)

@socketio.on('send_message')
def handle_send_message_event(data):
        app.logger.info("{} has sent a message to the room {}: {}".format(  data['user_name'], 
                                                                            data['chat_room_id'], 
                                                                            data['message']))
        socketio.emit('receive_message', data, chat_room_id = data['chat_room_id'])


# @chat_room_page.route("/chat_rooms/<chat_room_id>/receive", methods=['GET'])
# def receive_message():
#     pass

# @chat_room_page.route("/chat_rooms/<chat_room_id>/send", methods=['POST'])
# @login_required
# def send_message():
#     chat_room_id = request.form['chat_room_id']
#     user_id = request.form['user_id']
#     message_text = request.form['message_text']
#     message_datetime = request.form['datetime']
#     # message = Message(message_text,message_datetime)
#     #TODO post messages to server
#     # chat_room = FirestoreCollections.chat_rooms_ref().document(chat_room_id)


# @chat_room_page.route('/chat_rooms/join', methods=['POST'])
# def join_chat_room():
#     chat_room_id = request.form['chat_room_id']
#     user_id = request.form['user_id']
#     chat_room = FirestoreCollections.chat_rooms_ref().document(chat_room_id)
#     members = chat_room.data['members'].append(user_id)
#     chat_room.set({'members': members})
#     #TODO connect sockets

# @chat_room_page.route('/chat_rooms/join', methods=['POST'])
# def leave_chat_room():
#     pass

# @login_required
# @chat_room_page.route('/chat/new', methods=['POST'])
# def create_chat_room():
#     pass

# @login_required
# @chat_room_page.route('/chat/stop', methods=['POST'])
# def stop_chat_room():
#     pass

class ChatRoom:
    def __init__(self, chat_room_id, is_active):
        self.chat_room_id = chat_room_id
        self.members = []
        self.is_active = is_active

    def to_dict(self):
        return {'chat_room_id': self.chat_room_id,
                'members': self.members,
                'is_active': self.is_active}

    def store(self):
        FirestoreCollections.chat_rooms_ref().add(self.to_dict())

    class Message:
        def __init__(self, text, datetime):
            self.text = text
            self.datetime = datetime
        
        def to_dict(self):
            return {'text': self.text,
                    'datetime': self.datetime}
