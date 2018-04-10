from abc import abstractmethod, ABC
import tortilla


class EnvironmentSensor(ABC):
    """Base class for an environmental sensor"""

    @property
    @abstractmethod
    def internal_temperature(self):
        pass


class Photon(EnvironmentSensor):
    """
    Implements methods for a Particle-based environment sensor
    """

    def __init__(self, auth_token, device_id):
        self.auth_token = auth_token
        self.api = tortilla.wrap(f'https://api.particle.io/v1/devices/{device_id}')

    @property
    def internal_temperature(self):
        result = self.api.temperature.get(params={'access_token': self.auth_token})
        return float(result['result'])


