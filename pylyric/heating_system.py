from abc import abstractmethod, ABC


class HeatingSystem(ABC):
    """Base class for a heating system"""

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class Lyric(HeatingSystem):
    """
    Implements heating system methods for a Honeywell Lyric T6
    """
    ON_TEMPERATURE = 25
    OFF_TEMPERATURE = 15

    def __init__(self, device):
        """
        :param device: A Lyric T6 Device object
        """
        self.device = device

    def turn_on(self):
        self.device.change(mode="Heat", heatSetpoint=self.ON_TEMPERATURE, thermostatSetpointStatus="PermanentHold")

    def turn_off(self):
        self.device.change(mode="Off", heatSetpoint=self.OFF_TEMPERATURE, thermostatSetpointStatus="PermanentHold")
