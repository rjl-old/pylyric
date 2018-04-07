from pylyric.device import Device


class Boiler(Device):
    """This class represents a boiler"""

    def turn_on(self, low_celcius=20, high_celcius=22):
        url = "devices/thermostats/{}".format(self.device_id)
        payload = {
            'mode': 'Heat',
            "heatSetpoint": (high_celcius * 1.8) + 32,
            "coolSetpoint": (low_celcius * 1.8) + 32,
            "thermostatSetpointStatus": "PermanentHold"
        }

        self.lyric_api.post(url, payload=payload, locationId=self.location_id)
