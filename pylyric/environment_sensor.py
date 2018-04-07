from abc import abstractmethod, ABC
import requests


class EnvironmentSensor(ABC):
    """Base class for an environmental sensor"""

    @abstractmethod
    def internal_temperature(self):
        pass


class Particle(EnvironmentSensor):
    """
    Implements methods for a Particle-based environment sensor
    """

    def __init__(self):
        self.device_id = "37002b001147343438323536"

    @property
    def internal_temperature(self):
        url = f"https://api.particle.io/v1/devices/{self.device_id}/temperature"
        params = {"access_token": "51f8f2e01548da71585635f275914a49d383a4ae"}

        r = requests.get(url, params=params)
        temperature = float(r.json()['result'])
        return (temperature)
