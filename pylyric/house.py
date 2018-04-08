from datetime import datetime, timedelta

from pylyric.environment_sensor import EnvironmentSensor
from pylyric.heating_system import HeatingSystem


class House:
    """
    Represents a house with a heating system and an environemnt sensor
    """
    WARMUP_GRADIENT = 0.001637426900584798  # degC per minute
    COOLDOWN_GRADIENT = 0.001754760943355017  # degC per minute

    def __init__(self, heating_system: HeatingSystem=None, environment_sensor: EnvironmentSensor=None):
        self.heating_system = heating_system
        self.environment_sensor = environment_sensor

    def is_time_to_start_heating(self, required_temperature, current_temperature, required_time) -> bool:
        """
        Returns True if it is time to start heating the house
        :param required_temperature: (degC) float
        :param current_temperature: (degC) float
        :param required_time: datetime
        :return bool:
        """
        warm_up_time_mins = (required_temperature - current_temperature) / self.WARMUP_GRADIENT
        warm_up_time = timedelta(minutes=warm_up_time_mins)
        warm_up_start_time = required_time - warm_up_time

        return datetime.now() > warm_up_start_time

    def is_time_to_stop_heating(self, required_temperature, current_temperature, required_time) -> bool:
        """
        Returns True if it is time to stop heating the house
        :param required_temperature:
        :param current_temperature:
        :param required_time:
        :return:
        """
        cool_down_time_mins = (current_temperature - required_temperature) / self.COOLDOWN_GRADIENT
        cool_down_time = timedelta(minutes=cool_down_time_mins)
        cool_down_start_time = required_time - cool_down_time

        return datetime.now() > cool_down_start_time
