import os
import datetime
import requests
from requests.auth import HTTPBasicAuth


def make_expiry_date(seconds):
    """
    Returns a time that is 'seconds' seconds from now
    :param seconds: int
    :return: Datetime
    """
    return datetime.datetime.now() + datetime.timedelta(0, seconds)


class LyricOauthError(Exception):
    pass


class LyricClientCredentials:
    TOKEN_URL = "https://api.honeywell.com/oauth2/token"

    def __init__(self, client_id=None, client_secret=None, api_key=None, access_token=None, refresh_token=None,
                 redirect_url=None):
        """
        You can either provide a client_id and client_secret to the
        constructor or set LYRIC_CLIENT_ID and LYRIC_CLIENT_SECRET in
        environment variables
        :param client_id:
        :param client_secret:
        """

        if not client_id:
            client_id = os.getenv('LYRIC_CLIENT_ID')

        if not client_secret:
            client_secret = os.getenv('LYRIC_CLIENT_SECRET')

        if not api_key:
            api_key = os.getenv('LYRIC_API_KEY')

        if not access_token:
            access_token = os.getenv('LYRIC_ACCESS_TOKEN')

        if not refresh_token:
            refresh_token = os.getenv('LYRIC_REFRESH_TOKEN')

        if not redirect_url:
            redirect_url = os.getenv('LYRIC_REDIRECT_URL')

        if not client_id:
            raise LyricOathError('No client id')

        if not client_secret:
            raise LyricOauthError('No client secret')

        if not api_key:
            raise LyricOauthError('No api key')

        if not access_token:
            raise LyricOauthError('No access token')

        if not refresh_token:
            raise LyricOauthError('No refresh token')

        if not redirect_url:
            raise LyricOauthError('No redirect url')

        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.redirect_url = redirect_url
        self.expiry_date = None

    def get_access_token(self):
        if self._is_token_expired():
            self._refresh()
        return self.access_token

    def _is_token_expired(self):
        if self.expiry_date:
            return (self.expiry_date < datetime.datetime.now())
        else:
            return True

    def _refresh(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        r = requests.post(self.TOKEN_URL, auth=auth, data=payload)
        if r.status_code == 200:
            self.access_token = r.json()['access_token']
            self.expiry_date = make_expiry_date(int(r.json()['expires_in']))
        else:
            raise LyricOauthError("Couldn't refresh token: {}".format(r.json()))
