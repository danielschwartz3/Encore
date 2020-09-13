from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request, session
from login_required import login_required

user_page = Blueprint('user_page', __name__)


@login_required
@user_page.route("/api/users/all")
def get_all_users():
    docs = FirestoreCollections.users_ref().stream()
    return {doc.id: doc.to_dict() for doc in docs}


@login_required
@user_page.route("/api/user/genres", methods=['POST'])
def choose_genres():
    if request.method == 'POST':
        genres = request.form['genres']
        user_id = request.form['user_id']
        FirestoreCollections.users_ref().document(
            user_id).update({'genres': genres})


@login_required
@user_page.route("/api/user/<user_id>", methods=['GET'])
def get_user(user_id):
    if request.method == 'GET':
        return FirestoreCollections.users_ref().document(user_id).to_dict()


@user_page.route('/login', methods=['POST'])
def do_login():
    user = FirestoreCollections.user_ref()\
        .where(u'handle', u'===', request.form['handle'])\
        .where(u'hashed_password', u'===', request.form['hashed_password'])

    # session['logged_in'] = True if user else False
    session["user_id"] = user if user else None


@login_required
@user_page.route('/logout', methods=['POST'])
def do_logout():
    session.pop("user_id", None)


@user_page.route('/api/join', methods=['POST'])
def create_user():
    hashed_password = request.form['hashed_password']
    handle = request.form['handle']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    id = request.form['id']
    new_user = User(hashed_password, handle, email, first_name, last_name, id)
    new_user.store()


@login_required
@user_page.route('/api/users/add_friend', methods=['POST'])
def add_friend():
    my_id = request.form['user_id']
    friend_id = request.form['friend_id']
    
    friends = {'sent_by': my_id, 'to': friend_id, 'active': False}
    #check if friends exists first
    FirestoreCollections.friends_ref().add(friends)


@login_required
@user_page.route('/api/users/accept_friend', methods=['GET'])
def accept_friend():
    my_id = request.form['user_id']
    friend_id = request.form['friend_id']

    user = FirestoreCollections.users_ref().document(my_id)
    friends = FirestoreCollections.friends_ref().where(
        'sent_by', '===', friend_id).where('to', '===', my_id)
    friends.update({'active': True})
    reciprocal_friends = {'sent_by': my_id, 'to': friend_id, 'active': True}
    user.update({'friend_count': user.data['friend_count'] + 1})
    FirestoreCollections.friends_ref().add(reciprocal_friends)


@login_required
@user_page.route('/api/users/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    return {'friends': [doc.to_dict() for doc in FirestoreCollections.friends_ref().where('sent_by', '===', user_id)]}

@login_required
@user_page.route('/api/users/<user_id>/friendcount', methods=['GET'])
def friend_count(user_id):
    return {'friend_count': FirestoreCollections.users_ref().document(user_id).data['friend_count']}


@login_required
@user_page.route('/api/users/unfriend', methods=['POST'])
def unfriend():
    my_id = request.form['user_id']
    friend_id = request.form['friend_id']
    user = FirestoreCollections.users_ref().document(my_id)
    reciprocal_friends = FirestoreCollections.friends_ref().where(
        'sent_by', '===', friend_id).where('to', '===', my_id)
    friends = FirestoreCollections.friends_ref().where(
        'sent_by', '===', my_id).where('to', '===', friend_id)

    reciprocal_friends.update({'active': False})
    friends.update({'active': False})
    user.update({'friend_count': user.data['friend_count'] - 1})

@login_required
@user_page.route('/api/users/add_follower', methods=['POST'])
def add_follower():
    my_id = request.form['user_id']
    follower_id = request.form['follower_id']
    
    followers = {'sent_by': my_id, 'to': follower_id, 'active': False}
    #check if followers exists first
    FirestoreCollections.followers_ref().add(followers)


@login_required
@user_page.route('/api/users/accept_follower', methods=['GET'])
def accept_follower():
    my_id = request.form['user_id']
    follower_id = request.form['follower_id']

    user = FirestoreCollections.users_ref().document(my_id)
    followers = FirestoreCollections.followers_ref().where(
        'sent_by', '===', follower_id).where('to', '===', my_id)
    followers.update({'active': True})
    reciprocal_followers = {'sent_by': my_id, 'to': follower_id, 'active': True}
    user.update({'follower_count': user.data['follower_count'] + 1})
    FirestoreCollections.followers_ref().add(reciprocal_followers)


@login_required
@user_page.route('/api/users/<user_id>/followers', methods=['GET'])
def get_followers(user_id):
    return {'followers': [doc.to_dict() for doc in FirestoreCollections.followers_ref().where('sent_by', '===', user_id)]}

@login_required
@user_page.route('/api/users/<user_id>/followercount', methods=['GET'])
def follower_count(user_id):
    return {'follower_count': FirestoreCollections.users_ref().document(user_id).data['follower_count']}


@login_required
@user_page.route('/api/users/unfollow', methods=['POST'])
def unfollow():
    my_id = request.form['user_id']
    follower_id = request.form['follower_id']
    user = FirestoreCollections.users_ref().document(my_id)
    reciprocal_followers = FirestoreCollections.followers_ref().where(
        'sent_by', '===', follower_id).where('to', '===', my_id)
    followers = FirestoreCollections.followers_ref().where(
        'sent_by', '===', my_id).where('to', '===', follower_id)

    reciprocal_followers.update({'active': False})
    followers.update({'active': False})
    user.update({'follower_count': user.data['follower_count'] - 1})


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
