from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request
from datetime import datetime
from login_required import login_required
performance_page = Blueprint('performance_page', __name__)


@performance_page.route('/api/performances/all', methods=['GET'])
def get_all_performances():
    if request.method == 'GET':
        docs = FirestoreCollections.performances_ref().where(u'is_active' '==', True)
        return {doc.id: doc.to_dict() for doc in docs}


@login_required
@performance_page.route('/api/performances/new', methods=['POST'])
def create_performance():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = FirestoreCollections.users_ref().document(user_id)
        genres = user.get('genres')
        chat_room_id = request.form['chat_room_id']
        access_token = ""
        is_active = True
        performance = Performance(
            user_id, chat_room_id, genres, access_token, is_active)
        performance.store()


@login_required
@performance_page.route('/api/performances/stop', methods=['POST'])
def stop_performance():
    performance_id = request.form['performance_id']
    FirestoreCollections.performances_ref().document(
        performance_id).update({'is_active': False})


@performance_page.route('/api/performances/join', methods=['POST'])
def join_performance():
    performance_id = request.form['performance_id']
    user_id = request.form['user_id']
    performance_ref = FirestoreCollections.performances_ref().document(performance_id)
    total_views = performance_ref.get('total_views')
    current_views = performance_ref.get('current_views')
    audience = performance_ref.get('audience').append(user_id)
    performance_ref.update({'audience': audience})
    performance_ref.update({'total_views': total_views + 1})
    performance_ref.update({'current_views': current_views + 1})


@performance_page.route('/api/performances/join', methods=['POST'])
def leave_performance():
    performance_id = request.form['performance_id']
    user_id = request.form['user_id']
    performance_ref = FirestoreCollections.performances_ref().document(performance_id)
    total_views = performance_ref.get('total_views')
    audience = performance_ref.get('audience')
    audience.remove(user_id)
    performance_ref.update({'audience': audience})
    performance_ref.update({'total_views': total_views - 1})


@performance_page.route('/api/performances/<performance_id>/total_views', methods=['GET'])
def performance_total_views(performance_id):
    performance_ref = FirestoreCollections.performances_ref().document(performance_id)
    total_views = performance_ref.get('total_views')
    return {'total_views': total_views}

@performance_page.route('/api/performances/<performance_id>/viewcount', methods=['GET'])
def performance_current_views(performance_id):
    performance_ref = FirestoreCollections.performances_ref().document(performance_id)
    current_views = performance_ref.get('current_views')
    return {'current_views': current_views}


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
        self.total_views = 0
        self.current_views = 0

    def to_dict(self):
        return {'host_id': self.host_id,
                'chat_room_id': self.chat_room_id,
                'genres': self.genres,
                'time': self.time,
                'access_token': self.access_token,
                'title': self.title,
                'audience': self.audience,
                'is_active': self.is_active,
                'total_views': self.total_views,
                'current_views': self.current_views}

    def store(self):
        FirestoreCollections.performances_ref().add(self.to_dict())
