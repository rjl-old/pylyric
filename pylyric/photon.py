import dateutil.parser
from requests import Response

import server.config as config
from pylyric.environment_sensor import EnvironmentSensor
from pylyric.api_utils import protector, requests_retry_session

MAX_RETRIES = 3


class Photon(EnvironmentSensor):

    def __init__(self, device_id):
        self.device_id = device_id
        self.api = ParticleAPI()
        self.name = None
        self.notes = None
        self.connected = None
        self.last_heard = None
        self.variables = None
        self.functions = None
        self.last_ip_address = None

        self._parse_device_information()

    def _parse_device_information(self):
        response = self.api.get_device_information(self.device_id)
        json = response.json()
        self.name = json['name']
        self.notes = json['notes']
        self.connected = json['connected']
        self.last_heard = dateutil.parser.parse(json['last_heard'])
        self.variables = json['variables']
        self.functions = json['functions']
        self.last_ip_address = json['last_ip_address']
        self.json = json

    # EnvironmentSensor abstract function definitions

    @property
    def internal_temperature(self):
        # Assumes Photon firmware presents 'temperature' variable: modify as required
        variable_name = 'temperature'
        if variable_name not in self.variables:
            raise ValueError(f"Variable 'temperature' missing in photon {self.name}")
        else:
            response = self.api.get_variable(self.device_id, variable_name)
            return float(response.json()['result'])


class ParticleAPI:
    """Represents a Particle API client"""

    API_URL = 'https://api.particle.io/v1/devices/'

    def __init__(self):
        self.auth_token = config.PHOTON_AUTH_TOKEN

    @protector
    def get_device_information(self, device_id) -> Response:
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        return requests_retry_session().get(self._url(f'{device_id}'), headers=headers)

    @protector
    def get_variable(self, device_id, variable_name) -> Response:
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        return requests_retry_session().get(self._url(f'{device_id}/{variable_name}'), headers=headers)

    def _url(self, path):
        return self.API_URL + path
