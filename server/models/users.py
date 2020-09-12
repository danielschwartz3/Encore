from server.firestoreWrapper import Collections
from flask import Blueprint


user_page = Blueprint('user_page', __name__)


@user_page.route("/users")
def get_users():
    docs = Collections.users_ref().stream()
    return {'users': [doc.to_dict() for doc in docs]}
