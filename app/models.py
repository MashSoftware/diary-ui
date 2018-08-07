import json

import requests
from flask import Response, current_app

base_url = current_app.config.get('DIARY_API_URL')
version = current_app.config.get('DIARY_API_VERSION')
timeout = current_app.config.get('DIARY_API_TIMEOUT')


class User(object):

    def create(self, password, first_name, last_name, email_address):
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
            return Response(response=json.dumps({"message": "Request Timeout"}, separators=(',', ':')),
                            mimetype='application/json',
                            status=408)
        else:
            if response.status_code != 201:
                return Response(response=json.dumps({"message": "Failed to create user"}, separators=(',', ':')),
                                mimetype='application/json',
                                status=response.status_code)
            else:
                user = json.loads(response.text)
                return user

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
