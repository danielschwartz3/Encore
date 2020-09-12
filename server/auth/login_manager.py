"""
from flask_login import LoginManager
from app import app
from server.firestoreWrapper import FirestoreCollections
from server.models.users import User

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_data = FirestoreCollections.users_ref().document(user_id)
    if not user_data:
        return None
    else:
        return User.from_dict(user_data)
"""