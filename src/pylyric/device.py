import requests
import json

class Device:
    """Lyric Thermostat device."""

    def __init__(self, client, json):
        self.isAlive = json['isAlive']
        if self.isAlive == True:
            self.client = client
            self.json = json
            self.deviceID = json['deviceID']
            self.displayedOutdoorHumidity = float(json['displayedOutdoorHumidity'])
            self.indoorTemperature = float(json['indoorTemperature'])
            self.outdoorTemperature = float(json['outdoorTemperature'])
            self.operationStatus = json['operationStatus']['mode']

    def on(self, temperature):
        """Set heating on to temperature"""
        device_url = "https://api.honeywell.com/v2/devices/thermostats/{}".format(self.deviceID)
        headers = {
            "Authorization": "Bearer {}".format(self.client.access_token),
            "Content-Type": "application/json",
        }
        params = {
            "apikey": self.client.client_id,
            "locationId": 199754,
            }
        data = {
            "mode": "Heat",
            "heatSetpoint": temperature,
            "coolSetpoint": 1,
            "thermostatSetpointStatus": "TemporaryHold"
        }
        r = requests.post(device_url, headers=headers, params=params, data=json.dumps(data))
        print(r.request.url)
        if r.status_code == 200:
            return r
        else:
            raise ValueError("Couldn't set temperature: {}".format(r.json()))

    def off(self):
        """Set device heating off"""
        device_url = "https://api.honeywell.com/v2/devices/thermostats/{}".format(self.deviceID)
        headers = {
            "Authorization": "Bearer {}".format(self.client.access_token),
            "Content-Type": "application/json",
        }
        params = {
            "apikey": self.client.client_id,
            "locationId": 199754,
            }
        data = {
            "mode": "Off",
            "heatSetpoint": 16,
            "coolSetpoint": 1,
            "thermostatSetpointStatus": "TemporaryHold"
        }
        r = requests.post(device_url, headers=headers, params=params, data=json.dumps(data))
        print(r.request.url)
        if r.status_code == 200:
            return r
        else:
            raise ValueError("Couldn't set temperature: {}".format(r.json()))

