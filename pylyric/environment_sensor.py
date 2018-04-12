from abc import ABC, abstractmethod


class EnvironmentSensor(ABC):
    """Base class for an environmental sensor"""

    @property
    @abstractmethod
    def internal_temperature(self):
        pass
