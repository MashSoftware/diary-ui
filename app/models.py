import json

import requests
from werkzeug.exceptions import InternalServerError, RequestTimeout

from app import app, login
from flask_login import UserMixin

base_url = app.config.get('DIARY_API_URL')
version = app.config.get('DIARY_API_VERSION')
timeout = app.config.get('DIARY_API_TIMEOUT')


class User(UserMixin):

    def create(self, password, first_name, last_name, email_address):
        """Create a new user."""
        url = '{0}/{1}/users'.format(base_url, version)

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
                raise InternalServerError()
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def search(self, email_address):
        """Search for user by email address."""
        url = '{0}/{1}/users?email_address={2}'.format(base_url, version, email_address)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code == 404:
                return None
            elif response.status_code != 200:
                raise InternalServerError()
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def get(self, id):
        """Get a user."""
        url = '{0}/{1}/users/{2}'.format(base_url, version, str(id))
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 200:
                raise InternalServerError()
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def update_profile(self, id, first_name, last_name, email_address):
        """Update a user."""
        url = '{0}/{1}/users/{2}/profile'.format(base_url, version, str(id))

        updated_profile = {
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.put(url, data=json.dumps(updated_profile), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 200:
                raise InternalServerError()
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def change_password(self, id, current_password, new_password):
        """Update a user."""
        url = '{0}/{1}/users/{2}/password'.format(base_url, version, str(id))

        updated_profile = {
            "current_password": current_password,
            "new_password": new_password
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.put(url, data=json.dumps(updated_profile), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code == 401:
                return None
            # Need to handle 400's here too...
            elif response.status_code != 200:
                raise InternalServerError()
            else:
                user_dict = json.loads(response.text)
                user = self
                for k, v in user_dict.items():
                    setattr(user, k, v)
                return user

    def delete(self, id):
        """Delete a user."""
        url = '{0}/{1}/users/{2}'.format(base_url, version, str(id))
        headers = {"Accept": "application/json"}

        try:
            response = requests.delete(url, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 204:
                raise InternalServerError()
            else:
                return True

    def login(self, email_address, password):
        """Log in a user"""
        url = '{0}/{1}/auth/login'.format(base_url, version)

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

    def create(self, first_name, last_name, date_of_birth, users):
        """Create a new child."""
        url = '{0}/{1}/children'.format(base_url, version)

        new_child = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "users": users
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.post(url, data=json.dumps(new_child), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 201:
                raise InternalServerError()
            else:
                return json.loads(response.text)

    def get(self, id):
        """Get a child."""
        url = '{0}/{1}/children/{2}'.format(base_url, version, str(id))
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 200:
                raise InternalServerError()
            else:
                return json.loads(response.text)

    def update(self, id, first_name, last_name, date_of_birth, users):
        """Update a child."""
        url = '{0}/{1}/children/{2}'.format(base_url, version, str(id))

        updated_profile = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "users": users
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.put(url, data=json.dumps(updated_profile), headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 200:
                raise InternalServerError()
            else:
                return json.loads(response.text)

    def delete(self, id):
        """Delete a child."""
        url = '{0}/{1}/children/{2}'.format(base_url, version, str(id))
        headers = {"Accept": "application/json"}

        try:
            response = requests.delete(url, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code != 204:
                raise InternalServerError()
            else:
                return True


class Event(object):

    def create(self, event):
        pass

    def get(self, id):
        pass

    def get_for_child(self, child_id):
        """Get events for child."""
        url = '{0}/{1}/events?child_id={2}'.format(base_url, version, child_id)
        headers = {"Accept": "application/json"}

        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            raise RequestTimeout()
        else:
            if response.status_code == 404:
                return None
            elif response.status_code != 200:
                raise InternalServerError()
            else:
                return json.loads(response.text)

    def update(self, id):
        pass

    def delete(self, id):
        pass
