import json

import requests
from flask import Response
from werkzeug.exceptions import RequestTimeout

from app import app, login
from flask_login import UserMixin

base_url = app.config.get('DIARY_API_URL')
version = app.config.get('DIARY_API_VERSION')
timeout = app.config.get('DIARY_API_TIMEOUT')


class User(UserMixin):

    def create(self, password, first_name, last_name, email_address):
        """Create a new user."""
        url = '{0}/users'.format(base_url)

        new_user = {
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.post(url, data=json.dumps(new_user), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 201:
                return Response(response=json.dumps({"message": "Failed to create user"}, separators=(',', ':')),
                                mimetype='application/json',
                                status=response.status_code)
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def search(self, email_address):
        """Search for user by email address."""
        pass

    def get(self, id):
        """Get a user."""
        url = '{0}/users/{1}'.format(base_url, str(id))
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 200:
                return Response(response=json.dumps({"message": "Failed to retrieve user"}, separators=(',', ':')),
                                mimetype='application/json',
                                status=response.status_code)
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def update(self, id, first_name, last_name, email_address, password):
        """Update a user."""
        url = '{0}/users/{1}'.format(base_url, str(id))

        updated_user = {
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
            "password": password,
            "children": []
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.put(url, data=json.dumps(updated_user), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 200:
                return Response(response=json.dumps({"message": "Failed to update user"}, separators=(',', ':')),
                                mimetype='application/json',
                                status=response.status_code)
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def delete(self, id):
        """Delete a user."""
        pass

    def login(self, email_address, password):
        """Log in a user"""
        url = '{0}/login'.format(base_url)

        credentials = {
            "email_address": email_address,
            "password": password
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.post(url, data=json.dumps(credentials), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code == 401:
                return None
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user


@login.user_loader
def load_user(id):
    user = User()
    return user.get(id)


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


class Event(object):

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
