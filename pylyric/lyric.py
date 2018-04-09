import datetime
import server.config as config
import tortilla
import requests
from requests.auth import HTTPBasicAuth
from typing import List, Dict


class ApiCredentials:
    TOKEN_URL = "https://api.honeywell.com/oauth2/token"

    def __init__(self, client_id, client_secret, access_token, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expiry_date = None

    def get_access_token(self):
        if self._is_token_expired():
            self._refresh_token()
        return self.access_token

    def _is_token_expired(self) -> bool:
        return True if self.expiry_date is None else self.expiry_date < datetime.datetime.now()

    def _refresh_token(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)

        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }

        response = requests.post(self.TOKEN_URL, auth=auth, data=payload)

        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            self.expiry_date = self._date_seconds_from_now(int(response.json()['expires_in']))
        else:
            raise LyricOauthError(f"Couldn't refresh token: {response.json()}")

    @staticmethod
    def _date_seconds_from_now(seconds: int) -> datetime:
        return datetime.datetime.now() + datetime.timedelta(0, seconds)


class Device:
    """Represents a single Lyric device e.g a T6 thermostat."""

    def __init__(self, json):
        self.device_id = json['deviceID']
        self.name = json['name']
        self.indoor_temperature = float(json['indoorTemperature'])
        self.outdoor_temperature = float(json['outdoorTemperature'])
        self.outdoor_humidity = int(json['displayedOutdoorHumidity'])
        self.mode = json['operationStatus']['mode']
        self.changeable_values = json['changeableValues']


class Lyric:
    """Represents a Honeywell Lyric API client."""

    def __init__(self, config=config):
        self.auth = ApiCredentials(
                client_id=config.CLIENT_ID,
                client_secret=config.CLIENT_SECRET,
                access_token=config.ACCESS_TOKEN,
                refresh_token=config.REFRESH_TOKEN
        )
        self.api = tortilla.wrap('https://api.honeywell.com/v2/')

    @property
    def locations(self) -> List[Dict]:
        headers = {'Authorization': f'Bearer {self.auth.get_access_token()}'}
        params = {'apikey': self.auth.client_id}
        return self.api.locations.get(params=params, headers=headers)

    def devices(self, location_id) -> List[Device]:
        headers = {'Authorization': f'Bearer {self.auth.get_access_token()}'}
        params = {'apikey': self.auth.client_id, 'locationId': location_id}
        return [Device(json) for json in self.api.devices.get(params=params, headers=headers)]

    def device(self, location_id, device_id) -> Device:
        headers = {'Authorization': f'Bearer {self.auth.get_access_token()}'}
        params = {'apikey': self.auth.client_id, 'locationId': location_id}
        json = self.api.devices.thermostats(device_id).get(headers=headers, params=params)
        return Device(json)

    def change_device(self, location_id, device_id, **kwargs):
        device = self.device(location_id=location_id, device_id=device_id)
        changeable_values = device.changeable_values
        for k, v in kwargs.items():
            if k in changeable_values:
                changeable_values[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))
        headers = {'Authorization': f'Bearer {self.auth.get_access_token()}'}
        params = {'apikey': self.auth.client_id, 'locationId': location_id}
        data = changeable_values
        self.api.devices.thermostats(device_id).post(headers=headers, params=params, data=data)
