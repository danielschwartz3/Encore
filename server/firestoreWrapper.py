

from firebase_admin import credentials
import firebase_admin
from firebase_admin import firestore


cred = credentials.Certificate(
    'encore-1e5ea-firebase-adminsdk-qrpzn-39bbdd3196.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


class Collections(object):

    @staticmethod
    def chat_rooms_ref():
        return db.collection(u'chat_rooms')


    @staticmethod
    def follows_ref():
        return db.collection(u'follows')


    @staticmethod
    def friends_ref():
        return db.collection(u'friends')

    @staticmethod
    def genres_ref():
        return db.collection(u'genres')

    @staticmethod
    def messages_ref():
        return db.collection(u'messages')

    @staticmethod
    def performances_ref():
        return db.collection(u'messages')

    @staticmethod
    def scheduled_performances_ref():
        return db.collection(u'scheduled_performanes')
    
    @staticmethod
    def users_ref():
        return db.collection(u'users')


    
