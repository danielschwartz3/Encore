from server.firestoreWrapper import FirestoreCollections
from flask import Blueprint, request
from datetime import datetime


scheduled_performance_page = Blueprint('scheduled_performance_page', __name__)


@scheduled_performance_page.route('/performances/schedule', methods=['POST'])
def schedule_performance():
    if request.method == 'POST':
        datetime = request.form['datetime']
        host_id = request.form['user_id']
        genres = request.form['genres']
        title = request.form['title']
        scheduled_performance = ScheduledPerformance(datetime, host_id, genres, title)
        scheduled_performance.store()


class ScheduledPerformance():
    def __init__(self, datetime, host_id, genres, title):
        self.datetime, self.host_id, self.genres, self.title, self.rsvps = datetime, host_id, genres, title, []

    def to_dict(self):
        return {'datetime': self.datetime,
                'host_id': self.host_id,
                'genres': self.genres,
                'title': self.title,
                'rsvps': self.rsvps}

    def store(self):
        FirestoreCollections.scheduled_performances_ref().add(self.to_dict())
