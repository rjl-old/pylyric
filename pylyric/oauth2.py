import datetime
import os

from requests import post
from requests.auth import HTTPBasicAuth

TOKEN_URL = "https://api.honeywell.com/oauth2/token"

LYRIC_CLIENT_ID = "LYRIC_CLIENT_ID"
LYRIC_CLIENT_SECRET = "LYRIC_CLIENT_SECRET"
LYRIC_API_KEY = "LYRIC_API_KEY"
LYRIC_ACCESS_TOKEN = "LYRIC_ACCESS_TOKEN"
LYRIC_REFRESH_TOKEN = "LYRIC_REFRESH_TOKEN"
LYRIC_REDIRECT_URL = "LYRIC_REDIRECT_URL"


def date_seconds_from_now(seconds: int) -> datetime:
    """
    Returns a time that is n seconds from now.
    :param seconds: The number of seconds.
    :return: The datetime n seconds from now.
    """
    return datetime.datetime.now() + datetime.timedelta(0, seconds)


class LyricOauthError(Exception):
    pass


class LyricClientCredentials:

    def __init__(self, client_id=os.getenv(LYRIC_CLIENT_ID, None), client_secret=os.getenv(LYRIC_CLIENT_SECRET, None),
                 access_token=os.getenv(LYRIC_ACCESS_TOKEN, None), refresh_token=os.getenv(LYRIC_REFRESH_TOKEN, None)):
        """
        You can either provide a client_id and client_secret to the
        constructor or set LYRIC_CLIENT_ID and LYRIC_CLIENT_SECRET in
        environment variables
        :param client_id:
        :param client_secret:
        :param access_token:
        :param refresh_token:
        """

        parameter_dict = locals()

        for param in parameter_dict.keys():
            if parameter_dict[param] is None:
                raise LyricOauthError(f"No {param}.")

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expiry_date = None

    def get_access_token(self):
        """
        Gets an api token.
        :return: An access token.
        :raises LyricOauthError: Expired token can't be refreshed.
        """
        if self._is_token_expired():
            self._refresh()
        return self.access_token

    def _is_token_expired(self) -> bool:
        """
        Determines whether the current token is expired.
        """
        return True if self.expiry_date is None else self.expiry_date < datetime.datetime.now()

    def _refresh(self):
        """
        Refreshes the authentication token.
        :raises LyricOauthError: Problem with API.
        """
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = post(TOKEN_URL, auth=auth, data=payload)

        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.expiry_date = date_seconds_from_now(int(response.json()['expires_in']))
        else:
            raise LyricOauthError(f"Couldn't refresh token: {response.json()}")
