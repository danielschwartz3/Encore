from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request
from datetime import datetime

performance_page = Blueprint('performance_page', __name__)


@performance_page.route('/performances/all', methods=['GET'])
def get_all_performances():
    if request.method == 'GET':
        docs = FirestoreCollections.performances_ref().stream()
        return {doc.id: doc.to_dict() for doc in docs}


@performance_page.route('/performances/new', methods=['POST'])
def create_performance():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = FirestoreCollections.users_ref().document(user_id)
        genres = user.data['genres']
        chat_room_id = request.form['chat_room_id']
        access_token = ""
        performance = Performance(user_id, chat_room_id, genres, access_token)
        performance.store()

@performance_page.route('/performances/stop', methods='DELETE')
def stop_performance():
    pass

@performance_page.route('/performances/join', methods=['POST'])
def join_performance():
    pass


@performance_page.route('/performances/join', methods=['POST'])
def leave_performance():
    pass


class Performance:
    def __init__(self, host_id, chat_room_id, genres, access_token, title):
        self.host_id = host_id
        self.chat_room_id = chat_room_id
        self.genres = genres
        self.time = datetime.now()
        self.access_token = access_token
        self.title = title
        self.audience = []

    def to_dict(self):
        return {'host_id': self.host_id,
                'chat_room_id': self.chat_room_id,
                'genres': self.genres,
                'time': self.time,
                'access_token': self.access_token,
                'title': self.title,
                'audience': self.audience}

    def store(self):
        FirestoreCollections.performances_ref().add(self.to_dict())
