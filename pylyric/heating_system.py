from abc import ABC, abstractmethod


class HeatingSystem(ABC):
    """Base class for a heating system"""

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @property
    @abstractmethod
    def is_active(self) -> bool:
        pass