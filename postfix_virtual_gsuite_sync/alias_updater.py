from googleapiclient.discovery import build
from httplib2 import Http


SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'


class User:
    def __init__(self, service, user_id):
        self._service = service
        self.user_id = user_id

    @property
    def aliases(self):
        result = self._service.users().aliases().list(userKey=self.user_id).execute()
        return {
            alias['alias'] for alias in result.get('aliases', [])
        }

    def delete_alias(self, alias_address):
        self._service.users().aliases().delete(userKey=self.user_id, alias=alias_address).execute()

    def add_alias(self, alias_address):
        body = {
            'alias': alias_address,
            'kind': "admin#directory#alias",
        }
        result = self._service.users().aliases().insert(userKey=self.user_id, body=body).execute()
        return result['alias']


class Users:
    def __init__(self, service):
        self._service = service

    def get(self, user_id):
        return User(self._service, user_id)

    def __getitem__(self, item):
        user = self.get(item)
        if not user:
            raise KeyError(item)
        return user


class AliasUpdater:
    def __init__(self, google_api_creds):
        self._service = build('admin', 'directory_v1', http=google_api_creds.authorize(Http()))
        self.users = Users(self._service)

