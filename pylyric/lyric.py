import datetime
import server.config as config
import tortilla
import requests
from requests.auth import HTTPBasicAuth
from typing import List


class Device:
    """Represents a single Lyric device e.g a T6 thermostat."""

    # TODO: add update function to attributes

    def __init__(self, json, location_id, lyric):
        self.location_id = location_id
        self.device_id = json['deviceID']
        self.lyric = lyric
        self.name = json['name']

    @property
    def changeable_values(self):
        json = self._update()
        return json['changeableValues']

    @property
    def indoor_temperature(self):
        json = self._update()
        return float(json['indoorTemperature'])

    @property
    def outdoor_temperature(self):
        json = self._update()
        return float(json['outdoorTemperature'])

    @property
    def outdoor_humidity(self):
        json = self._update()
        return int(json['displayedOutdoorHumidity'])

    @property
    def mode(self):
        json = self._update()
        return json['operationStatus']['mode']

    def change(self, **kwargs):
        changeable_values = self.changeable_values
        for k, v in kwargs.items():
            if k in changeable_values:
                changeable_values[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))
        headers = {'Authorization': f'Bearer {self.lyric._get_access_token()}'}
        params = {'apikey': self.lyric.client_id, 'locationId': self.location_id}
        self.lyric.api.devices.thermostats(self.device_id).post(headers=headers, params=params, data=changeable_values)

    def _update(self):
        headers = {'Authorization': f'Bearer {self.lyric._get_access_token()}'}
        params = {'apikey': self.lyric.client_id, 'locationId': self.location_id}
        device_json = self.lyric.api.devices.thermostats(self.device_id).get(headers=headers, params=params)
        return device_json


class Lyric:
    """Represents a Honeywell Lyric API client."""

    TOKEN_URL = "https://api.honeywell.com/oauth2/token"

    def __init__(self, config=config):

        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET
        self.access_token = config.ACCESS_TOKEN
        self.refresh_token = config.REFRESH_TOKEN
        self.expiry_date = None

        self.api = tortilla.wrap('https://api.honeywell.com/v2/')

        self.devices = self._get_devices()

    def _get_devices(self) -> List[Device]:
        devices = []
        headers = {'Authorization': f'Bearer {self._get_access_token()}'}
        params = {'apikey': self.client_id}
        locations = self.api.locations.get(params=params, headers=headers)
        for location in locations:
            location_id = location['locationID']
            for device_json in location['devices']:
                devices.append(Device(json=device_json, location_id=location_id, lyric=self))
        return devices

    def _get_access_token(self) -> str:
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
            raise RuntimeError(f"Couldn't refresh token: {response.json()}")

    @staticmethod
    def _date_seconds_from_now(seconds: int) -> datetime:
        return datetime.datetime.now() + datetime.timedelta(0, seconds)
