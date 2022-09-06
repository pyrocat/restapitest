import requests
from requests import Request, Session, Response

from pprint import pprint

class ApiBrowser:
    def __init__(self,
                 login_url: str = None,
                 username: str = None,
                 key: str = None):

        self.username = username
        self.key = key
        self.token: str | None = None

        payload = {
            'username': username,
            'redmine_key': key
        }

        self._s = Session()

        try:
            r: Response = self._s.post(login_url, data=payload)
            self.token = 'Token ' + r.json()['token']
        except KeyError as err:
            print(err, r.json()['detail'])

        self._s.headers['Authorization'] = self.token


    def get(self, url):
        r = self._s.get(url)
        try:
            return r.json()
        except requests.exceptions.JSONDecodeError:  # In case an error occurs on the server
            return r.text

    def __del__(self):
        self._s.close()

def main():
    login_url = 'http://127.0.0.1:8000/api/token-auth/'
    username = 'johndoe'
    key = 'newfancyapikey'
    b = ApiBrowser(login_url=login_url, username=username, key=key)

    # Go to the root
    root = b.get('http://127.0.0.1:8000/')
    pprint(root)

    # Find all projects the user is a member of.
    projects_url = root['projects']
    projects = b.get(projects_url)
    pprint(projects)


if __name__ == '__main__':
    main()