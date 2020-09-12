from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request


user_page = Blueprint('user_page', __name__)


@user_page.route("/users/all")
def get_all_users():
    docs = FirestoreCollections.users_ref().stream()
    return {doc.id: doc.to_dict() for doc in docs}


@user_page.route("/user/genres", methods=['POST'])
def choose_genres():
    if request.method == 'POST':
        genres = request.form['genres']
        user_id = request.form['user_id']
        FirestoreCollections.users_ref().document(user_id).set({'genres': genres})


@user_page.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        return FirestoreCollections.users_ref().document(user_id).to_dict()

