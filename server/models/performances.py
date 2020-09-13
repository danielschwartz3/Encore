from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request
from datetime import datetime
from login_required import login_required
performance_page = Blueprint('performance_page', __name__)


@performance_page.route('/performances/all', methods=['GET'])
def get_all_performances():
    if request.method == 'GET':
        docs = FirestoreCollections.performances_ref().where(u'is_active' '===', True)
        return {doc.id: doc.to_dict() for doc in docs}


@login_required
@performance_page.route('/performances/new', methods=['POST'])
def create_performance():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = FirestoreCollections.users_ref().document(user_id)
        genres = user.data['genres']
        chat_room_id = request.form['chat_room_id']
        access_token = ""
        is_active = True
        performance = Performance(
            user_id, chat_room_id, genres, access_token, is_active)
        performance.store()


@login_required
@performance_page.route('/performances/stop', methods=['POST'])
def stop_performance():
    performance_id = request.form['performance_id']
    FirestoreCollections.performances_ref().document(
        performance_id).set({'is_active': False})


@performance_page.route('/performances/join', methods=['POST'])
def join_performance():
    performance_id = request.form['performance_id']
    user_id = request.form['user_id']
    performance = FirestoreCollections.performances_ref().document(performance_id)
    audience = performance.data['audience'].append(user_id)
    performance.set({'audience': audience})



@performance_page.route('/performances/join', methods=['POST'])
def leave_performance():
    performance_id = request.form['performance_id']
    user_id = request.form['user_id']
    performance = FirestoreCollections.performances_ref().document(performance_id)
    audience = performance.data['audience']
    audience.remove(user_id)
    performance.set({'audience': audience})


class Performance:
    def __init__(self, host_id, chat_room_id, genres, access_token, title, is_active):
        self.host_id = host_id
        self.chat_room_id = chat_room_id
        self.genres = genres
        self.time = datetime.now()
        self.access_token = access_token
        self.title = title
        self.audience = []
        self.is_active = is_active

    def to_dict(self):
        return {'host_id': self.host_id,
                'chat_room_id': self.chat_room_id,
                'genres': self.genres,
                'time': self.time,
                'access_token': self.access_token,
                'title': self.title,
                'audience': self.audience,
                'is_active': self.is_active}

    def store(self):
        FirestoreCollections.performances_ref().add(self.to_dict())
