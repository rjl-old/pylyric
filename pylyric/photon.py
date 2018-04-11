import dateutil.parser
import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import server.config as config
from pylyric.environment_sensor import EnvironmentSensor
from pylyric.utils import protector

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
        response = self.api.get_internal_temperature(self.device_id)
        return float(response.json()['result'])


class ParticleAPI:
    """Represents a Particle API client"""

    API_URL = 'https://api.particle.io/v1/devices/'

    def __init__(self):
        self.auth_token = config.PHOTON_AUTH_TOKEN

    @protector
    def get_device_information(self, device_id) -> Response:
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        return self.requests_retry_session().get(self._url(f'{device_id}'), headers=headers)

    @protector
    def get_internal_temperature(self, device_id) -> Response:
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        return self.requests_retry_session().get(self._url(f'{device_id}/temperature'), headers=headers)

    @staticmethod
    def requests_retry_session(
            retries=MAX_RETRIES,
            backoff_factor=0.3,
            status_forcelist=(400, 403, 404, 500, 503),
            session=None
    ) -> requests.Session:
        """see: https://www.peterbe.com/plog/best-practice-with-retries-with-requests"""
        session = session or requests.Session()
        retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                backoff_factor=backoff_factor,
                status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _url(self, path):
        return self.API_URL + path
