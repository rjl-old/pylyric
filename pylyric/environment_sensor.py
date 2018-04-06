import requests


class EnvironmentSensor:
    """Base class for an environmental sensor"""

    def __init__(self):
        self.endpoint = "https://api.particle.io/v1/devices"
        self.device_id = "37002b001147343438323536"
        self.access_token = "51f8f2e01548da71585635f275914a49d383a4ae"

    @property
    def internal_temperature(self):
        url = "{}/{}/temperature".format(self.endpoint, self.device_id)
        params = {"access_token": self.access_token}

        r = requests.get(url, params=params)
        temperature = float(r.json()['result'])
        return (temperature)
