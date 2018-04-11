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
        resp = self.requests_retry_session().post(
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
        token = self._get_auth_token().json()["access_token"]
        headers = {'Authorization': f'Bearer {token}'}
        params = {'apikey': self.client_id}
        return self.requests_retry_session().get(self._url('locations'), headers=headers, params=params)

    @staticmethod
    def requests_retry_session(
            retries=MAX_RETRIES,
            backoff_factor=0.3,
            status_forcelist=(400, 403, 404, 500),
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
