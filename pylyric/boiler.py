import requests
from requests.auth import HTTPBasicAuth
import datetime

from pylyric.oauth2 import

def date_seconds_from_now(seconds: int) -> datetime:
    """
    Returns a time that is n seconds from now.
    :param seconds: The number of seconds.
    :return: The datetime n seconds from now.
    """
    return datetime.datetime.now() + datetime.timedelta(0, seconds)

class Boiler:
    """This class represents a boler"""

    HONEYWELL_API = "https://api.honeywell.com/v2/"
    LOCATION_ID = "199754"
    DEVICE_ID = "LCC-00D02DB6B4A8"
    TOKEN_URL = "https://api.honeywell.com/oauth2/token"

    def __init__(self):
        self.consumer_key = "2IvMPqBmBBDhl3vBWVbCs4IvqjfQ9AUZ"
        self.consumer_secret = "lmVks7zDAdyoRQOT"
        self.access_token = "AZJyWOGjxUVtpGQ2w7jNA9EdWu8O"
        self.refresh_token = "G84Tia8JeST2ELVBqWQWRdZ4cQuqWKZM"
        self.expiry_date = None
        self.location_id = "199754"

    def turn_on(self):
        url = self.HONEYWELL_API + "devices/thermostats/{}".format(self.DEVICE_ID)
        headers = {'Authorization': self.get_access_token(), 'Content-Type': 'application/json'}
        params = {'apikey': self.client_id, 'locationID': self.location_id}
        data = {'mode': 'Heat'}
        r = requests.post(url, headers=headers, params=params, data=data)
        print(r.headers)

    def get_access_token(self):
        if self._is_token_expired():
            self._refresh_token()
        return self.access_token

    def _is_token_expired(self) -> bool:
        return True if self.expiry_date is None else self.expiry_date < datetime.datetime.now()

    def _refresh_token(self):
        auth = HTTPBasicAuth(self.consumer_key, self.consumer_secret)
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        response = requests.post(self.TOKEN_URL, auth=auth, data=payload)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.expiry_date = date_seconds_from_now(int(response.json()['expires_in']))
        else:
            raise  ValueError(f"Couldn't refresh token: {response.json()}")

