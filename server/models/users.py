from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request, session


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
        FirestoreCollections.users_ref().document(
            user_id).set({'genres': genres})


@user_page.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        return FirestoreCollections.users_ref().document(user_id).to_dict()


@user_page.route('/login', methods=['POST'])
def do_login():
    user = FirestoreCollections.user_ref()\
        .where(u'username', u'===', request.form['username'])\
        .where(u'hashed_password', u'===', request.form['hashed_password'])

    session['logged_in'] = True if user else False

@user_page.route('/logout', methods=['POST'])
def do_logout():
    pass

@user_page.route('/join', methods=['POST'])
def create_user():
    hashed_password = request.form['hashed_password']
    handle = request.form['handle']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    new_user = User(hashed_password, handle, email, first_name, last_name)
    new_user.store()


class User(object):
    def __init__(self, hashed_password, handle, email, first_name, last_name):
        self.hashed_password, self.handle, self.email, self.first_name, self.last_name = hashed_password, handle, email, first_name, last_name
        self.score = 1

    def to_dict(self):
        return {"hashed_password": self.hashed_password,
                "handle": self.handle,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name}

    def store(self):
        FirestoreCollections.users_ref().add(self.to_dict())
