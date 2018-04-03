import requests
import json

class Device:
    """
    This class represents a Lyric Thermostat device.
    """

    def __init__(self, client, json):
        self.isAlive = json['isAlive']
        if self.isAlive == True:
            self.client = client
            self.json = json
            self.deviceID = json['deviceID']

            self.outdoorHumidity = None
            self.indoorTemperature = None
            self.outdoorTemperature = None
            self.is_heating = None

            self.changeableValues = None
            # coolSetpoint
            # endCoolSetpoint
            # heatSetpoint
            # endHeatSetpoint
            # heatCoolMode
            # holdUntil
            # mode
            # nextPeriodTime : Indicates when next schedule period starts
            # thermostatSetpointStatus : TemporaryHold, HoldUntil, PermanentHold, VacationHold, NoHold

            self.update()

    def update(self):
        device_url = "https://api.honeywell.com/v2/devices/thermostats/{}".format(self.deviceID)
        headers = {"Authorization": "Bearer {}".format(self.client.access_token)}
        params = {
            "apikey": self.client.client_id,
            "locationId": 199754,
            }
        r = requests.get(device_url, headers=headers, params=params)
        if r.status_code == 200:
            json = r.json()
            self.outdoorHumidity = int(json['displayedOutdoorHumidity'])
            self.indoorTemperature = float(json['indoorTemperature'])
            self.outdoorTemperature = float(json['outdoorTemperature'])
            if json['operationStatus']['mode'] == "Heat":
                self.is_heating = True
            else:
                self.is_heating = False
            self.changeableValues = json['changeableValues']
        else:
            raise ValueError("Couldn't update device: {}".format(r.json()))

    def change(self,
               heatSetpoint=None,
               endHeatSetpoint=None,
               holdUntil=None,
               mode=None,
               nextPeriodTime=None,
               thermostatSetpointStatus=None,
               ):
        """Change changeable values"""
        self.update()


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

