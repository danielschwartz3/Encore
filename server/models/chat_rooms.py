# from server.firestoreWrapper import FirestoreCollections
# from flask import Blueprint, request
# from flask import Flask
# from flask_socketio import SocketIO
# from login_required import login_required
# from app import socketio

# chat_room_page = Blueprint('chat_room_page', __name__)

# @chat_room_page.route("/chat_rooms", methods=['GET'])
# def get_all_chat_rooms():
#     docs = FirestoreCollections.chat_rooms_ref().stream()
#     return {'chat_rooms': [doc.to_dict() for doc in docs]}

# @socketio.on('join_room')
# def handle_join_room_event(data): #TODO ensure that right info is passed in
#     chat_room_id = request.form['chat_room_id']
#     user_handle = request.form['user_handle']
#     chat_room_page.logger.info("{} has joined the chat".format(user_handle))
#     #TODO join_room(chat_room_id)
#     socketio.emit('join_room_announcement', data)

# @socketio.on('send_message')
# def handle_send_message_event(data):
#         chat_room_page.logger.info("{} has sent a message to the chat: {}".format(data['handle'], data['message']))
#         socketio.emit('receive_message', data, chat_room_id = data['chat_room_id'])


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

# class ChatRoom:
#     def __init__(self, chat_room_id, is_active):
#         self.chat_room_id = chat_room_id
#         self.members = []
#         self.is_active = is_active

#     def to_dict(self):
#         return {'chat_room_id': self.chat_room_id,
#                 'members': self.members,
#                 'is_active': self.is_active}

#     def store(self):
#         FirestoreCollections.chat_rooms_ref().add(self.to_dict())

#     class Message:
#         def __init__(self, text, datetime):
#             self.text = text
#             self.datetime = datetime
        
#         def to_dict(self):
#             return {'text': self.text,
#                     'datetime': self.datetime}