import json
import os
import re
import requests
from requests.auth import HTTPBasicAuth
from pylyric.device import Device

auth_url = "https://api.honeywell.com/oauth2/authorize"
token_url = "https://api.honeywell.com/oauth2/token"

class Lyric:
    """
    This class provides a client for managing Honeywell 'Lyric' devices.
    """

    def __init__(self):
        config_file = os.path.join((os.path.abspath(os.path.dirname(__file__))), "auth.json")
        with open(config_file) as json_file:
            config_data = json.load(json_file)
            # client data
            self.client_id = config_data['client']['client_id']
            self.client_secret = config_data['client']['client_secret']
            self.api_key = config_data['client']['api_key']
            self.redirect_url = config_data['client']['redirect_url']
            # token data
            self.access_token = config_data['tokens']['access_token']
            self.refresh_token = config_data['tokens']['refresh_token']

        self.refresh_tokens()


    def _get_authorisation_code(self):
        """Get an authorisation code to access authorisation tokens"""
        auth_request_url = "{}?response_type=code&client_id={}&redirect_uri={}".format(auth_url, self.client_id,
                                                                                       self.redirect_url)

        # print authorization link and get response
        print('Please go to:\n\n%s\n\nand authorize access.\n' % auth_request_url)
        authorization_response = input('\nEnter the full callback URL:\n')

        # get code from response
        m = re.search('\?code=(.*)\&scope=', authorization_response)
        code = m.group(1)
        print("> Got code: {}".format(code))
        return code

    def get_tokens(self):
        """
        Get access tokens.
        This requires user to open the browser and supply a url at the prompt
        """
        authorisation_code = self._get_authorisation_code()
        data = {
            "grant_type": "authorization_code",
            "code": authorisation_code,
            "redirect_uri": self.redirect_url
        }
        r = requests.post(token_url, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=data)

        if r.status_code == 200:
            tokens = r.json()
            self.access_token = tokens["access_token"]
            self.refresh_token = tokens["refresh_token"]
        else:
            raise ValueError("Couldn't get token: {}".format(r.json()))

    def refresh_tokens(self):
        """
        Refresh authorisation token.
        """
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        r = requests.post(token_url, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=data)
        if r.status_code == 200:
            self.access_token = r.json()['access_token']
            print("> Refreshed access token: {}".format(self.access_token))
        else:
            raise ValueError("Couldn't refresh token: {}".format(r.json()))

    def _get(self, url, headers, params):
        r = requests.get(devices_url, headers=headers, params=params)
        if r.status_code == 200:
            return [Device(client=self, json=json) for json in r.json()]
            # return r.json()
        else:
            raise ValueError("Couldn't get devices: {}".format(r.json()))



    @property
    def locations(self):
        """
        :return: dictionary with location data
        """
        locations_url = "https://api.honeywell.com/v2/locations"
        headers = {"Authorization": "Bearer {}".format(self.access_token)}
        params = {"apikey": self.client_id}

        r = requests.get(locations_url, headers=headers, params=params)
        print(r.url)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError("Couldn't get locations: {}".format(r.json()))

    def devices(self, locationID):
        """
        :param locationID: int
        :return: list of Device
        """
        devices_url = "https://api.honeywell.com/v2/devices"
        headers = {"Authorization": "Bearer {}".format(self.access_token)}
        params = {
            "apikey": self.client_id,
            "locationId": locationID
        }

        r = requests.get(devices_url, headers=headers, params=params)
        if r.status_code == 200:
            return [Device(client=self, json=json) for json in r.json()]
            # return r.json()
        else:
            raise ValueError("Couldn't get devices: {}".format(r.json()))

    def device(self, deviceID):
        """
        :param deviceID: Device ID
        :return: Device
        """
        device_url = "https://api.honeywell.com/v2/devices/thermostats/{}".format(deviceID)
        headers = {"Authorization": "Bearer {}".format(self.access_token)}
        params = {
            "apikey": self.client_id,
            "locationId": self.locations[0]['locationID']
            }
        r = requests.get(device_url, headers=headers, params=params)
        if r.status_code == 200:
            return Device(client=self, json=r.json())
            # return r.json()
        else:
            raise ValueError("Couldn't set device: {}".format(r.json()))

