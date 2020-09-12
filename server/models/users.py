from server.firestoreWrapper import Collections
from flask import Blueprint, request


user_page = Blueprint('user_page', __name__)




@user_page.route("/users")
def get_all_users():
    docs = Collections.users_ref().stream()
    return {'users': [doc.to_dict() for doc in docs]}


class User:


    @user_page.route("/user/<user_id>/genres", methods = ['POST'])
    def choose_genres(user_id):
        if request.method == 'POST':
            genres = request.form['genres']
            Collections.users_ref().document(user_id).set({'genres': genres})


    @user_page.route("/user/<user_id>", methods = ['GET'])
    def get_user(user_id):
        if request.method == 'GET':
            return Collections.users_ref().document(user_id).to_dict()