from abc import abstractmethod, ABC
import requests
import server.config as cfg
from pylyric.particle import Particle


class EnvironmentSensor(ABC):
    """Base class for an environmental sensor"""

    @property
    @abstractmethod
    def internal_temperature(self):
        pass


class Photon(Particle, EnvironmentSensor):
    """
    Implements methods for a Particle-based environment sensor
    """

    @property
    def internal_temperature(self):
        return self.internal_temperture
