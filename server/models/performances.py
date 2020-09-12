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
        time = datetime.now()

        FirestoreCollections.performances_ref().add(
            {u'user_id': user_id, u'time': time, u'genres': genres})
