import json
import os
import re
import requests
from requests.auth import HTTPBasicAuth

auth_url = "https://api.honeywell.com/oauth2/authorize"
token_url = "https://api.honeywell.com/oauth2/token"


class Lyric:

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

    def _get_authorisation_code(self):
        """get authorisation code to access authorisation tokens"""
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
        """get and print access tokens"""
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
            print("> Got tokens")
        else:
            raise ValueError("Couldn't get token: {}".format(r.json()))

    def refresh_tokens(self):
        """Refresh authorisation token"""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token}

        r = requests.post(token_url, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=data)
        if r.status_code == 200:
            self.access_token = r.json()['access_token']
            print("> Refreshed access token: {}".format(self.access_token))
        else:
            raise ValueError("Couldn't refresh token: {}".format(r.json()))

    def refresh(self):
        """Refresh access token"""
        api_url = "https://api.honeywell.com/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        r = requests.post(api_url, auth=HTTPBasicAuth(self.client_id, self.client_secret), data=data)
        if r.status_code == 200:
            self.access_token = r.json()['access_token']
        else:
            raise ValueError("Couldn't refresh token")

    @property
    def locations(self):
        api_url = "https://api.honeywell.com/v2/locations"
        headers = {"Authorization": "Bearer sKnEGqauCniWNA1i2XUM5GwTPT4b"}
        params = {"apikey": self.api_key}
        r = requests.get(api_url, headers=headers, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError("Couldn't get locations")

    def dummy(self):
        data = [{'locationID': 199754, 'name': 'Kingswood', 'streetAddress': '13A Clermiston Road North',
                 'city': 'Edinburgh', 'country': 'Canada', 'zipcode': 'EH4 7BL', 'devices': [
                {'displayedOutdoorHumidity': 86, 'vacationHold': {'enabled': False},
                 'currentSchedulePeriod': {'day': 'Monday', 'period': 'P4'},
                 'scheduleCapabilities': {'availableScheduleTypes': ['None', 'Geofenced', 'TimedEmea'],
                                          'schedulableFan': False},
                 'scheduleType': {'scheduleType': 'Timed', 'scheduleSubType': 'EMEA'}, 'scheduleStatus': 'Resume',
                 'allowedTimeIncrements': 10, 'settings': {'hardwareSettings': {'brightness': 2, 'maxBrightness': 5},
                                                           'temperatureMode': {'air': True}, 'specialMode': {}},
                 'deviceClass': 'Thermostat', 'deviceType': 'Thermostat', 'deviceID': 'LCC-00D02DB6B4A8',
                 'userDefinedDeviceName': 'Lyric T6 Thermostat', 'name': 'Lyric T6 Thermostat', 'isAlive': True,
                 'isUpgrading': False, 'isProvisioned': True, 'macID': '00D02DB6B4A8', 'deviceSettings': {},
                 'units': 'Celsius', 'indoorTemperature': 22, 'outdoorTemperature': 3, 'allowedModes': ['Heat', 'Off'],
                 'deadband': 0, 'hasDualSetpointStatus': False, 'minHeatSetpoint': 5, 'maxHeatSetpoint': 35,
                 'minCoolSetpoint': -18, 'maxCoolSetpoint': -18,
                 'changeableValues': {'mode': 'Heat', 'heatSetpoint': 16, 'coolSetpoint': 10,
                                      'thermostatSetpointStatus': 'NoHold', 'nextPeriodTime': '06:30:00',
                                      'endHeatSetpoint': 16, 'endCoolSetpoint': 10, 'heatCoolMode': 'Heat'},
                 'operationStatus': {'mode': 'EquipmentOff', 'fanRequest': False, 'circulationFanRequest': False}}],
                 'users': [{'userID': 237054, 'username': 'richardlyon@fastmail.com', 'firstname': 'Richard',
                            'lastname': 'Lyon', 'created': 1489517333, 'deleted': -62135596800, 'activated': True,
                            'connectedHomeAccountExists': True, 'locationRoleMapping': [
                         {'locationID': 199754, 'role': 'Adult', 'locationName': 'Kingswood', 'status': 1}],
                            'isCurrentUser': True},
                           {'userID': 319625, 'username': 'arlyon@me.com', 'firstname': 'Alexander', 'lastname': 'Lyon',
                            'created': 1497089136, 'deleted': -62135596800, 'activated': True,
                            'connectedHomeAccountExists': True, 'locationRoleMapping': [
                               {'locationID': 199754, 'role': 'Adult', 'locationName': 'Kingswood', 'status': 1}],
                            'isCurrentUser': False}], 'timeZone': 'GMT Standard Time', 'ianaTimeZone': 'Europe/London',
                 'daylightSavingTimeEnabled': True, 'geoFences': [
                {'geoFenceID': 202528, 'latitude': 55.96083, 'longitude': -3.28103781, 'radius': 500,
                 'geoOccupancy': {'withinFence': 0, 'outsideFence': 1}}], 'geoFenceEnabled': True,
                 'geoFenceNotificationEnabled': True}]
        return data
