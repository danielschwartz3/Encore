from flask_login.utils import login_required, logout_user
from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request
from flask_login import login_user, logout_user

user_page = Blueprint('user_page', __name__)

@login_required
@user_page.route("/users/all")
def get_all_users():
    docs = FirestoreCollections.users_ref().stream()
    return {doc.id: doc.to_dict() for doc in docs}

@login_required
@user_page.route("/user/genres", methods=['POST'])
def choose_genres():
    if request.method == 'POST':
        genres = request.form['genres']
        user_id = request.form['user_id']
        FirestoreCollections.users_ref().document(
            user_id).set({'genres': genres})

@login_required
@user_page.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        return FirestoreCollections.users_ref().document(user_id).to_dict()


@user_page.route('/login', methods=['POST'])
def do_login():
    user_data = FirestoreCollections.user_ref()\
        .where(u'handle', u'===', request.form['handle'])\
        .where(u'hashed_password', u'===', request.form['hashed_password'])

    user = User.from_dict(user_data.to_dict())
    login_user(user)

@login_required
@user_page.route('/logout', methods=['POST'])
def do_logout():
    logout_user()


@user_page.route('/join', methods=['POST'])
def create_user():
    hashed_password = request.form['hashed_password']
    handle = request.form['handle']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    id = request.form['id']
    new_user = User(hashed_password, handle, email, first_name, last_name, id)
    new_user.store()


class User(object):
    def __init__(self, hashed_password, handle, email, first_name, last_name, id):
        self.hashed_password, self.handle, self.email, self.first_name, self.last_name, self.id = hashed_password, handle, email, first_name, last_name, id
        self.score = 1
        self.genres = []
        self.is_active = True
    def to_dict(self):
        return {"hashed_password": self.hashed_password,
                "handle": self.handle,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "genres": [],
                "is_active": self.is_active}


    @staticmethod
    def from_dict(data):
        hashed_password = data['hashed_password']
        handle = data['handle']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        id = data['id']
        return User(hashed_password, handle, email, first_name, last_name, id)

    def store(self):
        FirestoreCollections.users_ref().add(self.to_dict())


    @property
    def is_authenticated(self):
            user = FirestoreCollections.user_ref()\
        .where(u'handle', u'===', self.handle)\
        .where(u'hashed_password', u'===', self.hashed_password)

    @property
    def is_active(self):
        return self.is_active
    
    @property
    def is_annonymous(self):
        return False

    def get_id(self):
        return str(self.id)


