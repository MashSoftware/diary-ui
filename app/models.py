import json
import requests
from flask import current_app

base_url = current_app.config.get('DIARY_API_URL')
version = current_app.config.get('DIARY_API_VERSION')
timeout = current_app.config.get('DIARY_API_TIMEOUT')


class User(object):

    def create(self, user):
        pass

    def search(self, query):
        pass

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass

    def delete(self, user_id):
        pass


class Child(object):

    def create(self, child):
        pass

    def search(self, query):
        pass

    def get(self, child_id):
        pass

    def update(self, child_id):
        pass

    def delete(self, child_id):
        pass


class Event (object):

    def create(self, event):
        pass

    def search(self, query):
        pass

    def get(self, event_id):
        pass

    def update(self, event_id):
        pass

    def delete(self, event_id):
        pass
