import requests


class EnvironmentSensor:
    """Base class for an environmental sensor"""

    @property
    def internal_temperature(self):
        url = "https://api.particle.io/v1/devices/37002b001147343438323536/temperature"
        params = {"access_token": "51f8f2e01548da71585635f275914a49d383a4ae"}

        r = requests.get(url, params=params)
        temperature = float(r.json()['result'])
        return (temperature)
