from typing import List

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.util.retry import Retry

import server.config as config
from pylyric.heating_system import Device
from pylyric.utils import protector

MAX_RETRIES = 3


class Lyric:
    """Class for managing Lyric devices"""

    def __init__(self):
        self.api = LyricAPI()
        self.devices = self._get_devices()

    def _get_devices(self) -> List[Device]:
        devices = []
        locations = self.api.get_locations().json()
        for location in locations:
            location_id = location['locationID']
            for device_json in location['devices']:
                devices.append(Device(json=device_json, location_id=location_id, lyric=self))
        return devices


class LyricAPI:
    """Represents a Honeywell Lyric API client"""

    TOKEN_URL = "https://api.honeywell.com/oauth2/token"
    API_URL = "https://api.honeywell.com/v2/"

    def __init__(self):
        self.client_id = config.CLIENT_ID
        self.client_secret = config.CLIENT_SECRET
        self.refresh_token = config.REFRESH_TOKEN

    @protector
    def _get_auth_token(self) -> Response:
        resp = requests_retry_session().post(
                self.TOKEN_URL,
                auth=HTTPBasicAuth(self.client_id, self.client_secret),
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token
                }
        )
        return resp

    @protector
    def get_locations(self) -> Response:
        url = self._url('locations')
        token = self._get_auth_token().json()["access_token"]
        headers = {'Authorization': f'Bearer {token}'}
        params = {'apikey': self.client_id}
        return requests_retry_session().get(url, headers=headers, params=params)

    @protector
    def get_thermostat(self, location_id, device_id) -> Response:
        url = self._url(f'devices/thermostats/{device_id}')
        token = self._get_auth_token().json()["access_token"]
        headers = {'Authorization': f'Bearer {token}'}
        params = {
            'apikey': self.client_id,
            'locationId': location_id
        }
        return requests_retry_session().get(url, headers=headers, params=params)

    @protector
    def change_thermostat(self, location_id, device_id, **kwargs) -> Response:
        # get the current state
        result = self.get_thermostat(location_id=location_id, device_id=device_id).json()
        changeable_values = result['changeableValues']

        # update dictionary with new parameters
        for k, v in kwargs.items():
            if k in changeable_values:
                changeable_values[k] = v
            else:
                raise ValueError("Unknown parameter: '{}'".format(k))

        # update device
        url = self._url(f'devices/thermostats/{device_id}')
        token = self._get_auth_token().json()["access_token"]
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        params = {
            'apikey': self.client_id,
            'locationId': location_id
        }
        data = json.dumps(changeable_values)
        return requests_retry_session().post(url, headers=headers, params=params, data=data)

    def _url(self, path):
        return self.API_URL + path
