from abc import abstractmethod, ABC

from pylyric.device import Device


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
    def on(self):
        pass


class T6(Device, HeatingSystem):
    """
    Implements heating system methods for a Honeywell Lyric T6
    """

    ON_TEMPERATURE = 25
    OFF_TEMPERATURE = 15

    def turn_on(self):
        self._on = True
        self.change(mode="Heat", heatSetpoint=self.ON_TEMPERATURE, thermostatSetpointStatus="PermanentHold")

    def turn_off(self):
        self._off = False
        self.change(mode="Off", heatSetpoint=self.OFF_TEMPERATURE, thermostatSetpointStatus="PermanentHold")

    @property
    def on(self) -> bool or None:
        return self._on if self._on else None
