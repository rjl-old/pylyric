from abc import abstractmethod, ABC
from sanic.log import logger
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
        try:
            MAX_TRIES = 3
            tries = 0
            result = None
            while tries < MAX_TRIES:
                try:
                    result = self.api.temperature.get(params={'access_token': self.auth_token})
                    result = float(result['result'])
                    break
                except Exception as e:
                    tries += 1
                    logger.warn("Failed to get Photon temperature - retrying")
            return result
        except:
            logger.error("PHOTON.internal_temperature EXCEPTION")



