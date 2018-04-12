import json
from typing import List

from requests import Response
from requests.auth import HTTPBasicAuth

import server.config as config
from pylyric.api_utils import protector, requests_retry_session
from pylyric.environment_sensor import EnvironmentSensor
from pylyric.heating_system import HeatingSystem


class Device(HeatingSystem, EnvironmentSensor):
    ON_TEMPERATURE = 25  # degC - arbitrary, just need 'hot'
    OFF_TEMPERATURE = 15  # degC - arbitrary, just need 'cold'

    def __init__(self, json, location_id, api):
        self.device_id = json['deviceID']
        self.name = json['name']
        self.location_id = int(location_id)
        self.api = api
        self._on = None

    # HeatingSystem abstract function definitions

    def turn_on(self):
        self.api.change_thermostat(
                location_id=self.location_id,
                device_id=self.device_id,
                mode="Heat",
                heatSetpoint=self.ON_TEMPERATURE,
                thermostatSetpointStatus="PermanentHold"
        )

    def turn_off(self):
        self.api.change_thermostat(
                location_id=self.location_id,
                device_id=self.device_id,
                mode="Off",
                heatSetpoint=self.OFF_TEMPERATURE,
                thermostatSetpointStatus="PermanentHold"
        )

    @property
    def is_on(self) -> bool:
        response = self.api.get_thermostat(location_id=self.location_id, device_id=self.device_id)
        string = response.json()['operationStatus']['mode']
        return True if string == 'Heat' else False

    # EnvironmentSensor function definitions

    @property
    def internal_temperature(self):
        response = self.api.get_thermostat(location_id=self.location_id, device_id=self.device_id)
        return float(response.json()['indoorTemperature'])

    # Other methods

    @property
    def mode(self):
        response = self.api.get_thermostat(location_id=self.location_id, device_id=self.device_id)
        return str(response.json()['changeableValues']['mode'])




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
                devices.append(Device(json=device_json, location_id=location_id, api=self.api))
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
