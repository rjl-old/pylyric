from datetime import datetime, timedelta

from pylyric.environment_sensor import EnvironmentSensor
from pylyric.heating_system import HeatingSystem
from pylyric.schedule import Schedule


class House:
    """
    Represents a house with a heating system and an environment sensor
    """
    WARMUP_GRADIENT = 0.001637426900584798  # degC per minute
    COOLDOWN_GRADIENT = -0.001825459656038644  # degC per minute

    def __init__(self,
                 heating_system: HeatingSystem = None,
                 environment_sensor: EnvironmentSensor = None,
                 schedule: Schedule = None,
                 ):
        self.heating_system = heating_system
        self.environment_sensor = environment_sensor
        self.schedule = schedule

    @property
    def is_time_to_warm_up(self) -> bool:
        """
        Returns True if it is time to start heating the house
        """
        required_temperature = self.schedule.active_period_minimum_temperature
        current_temperature = self.environment_sensor.internal_temperature
        required_time = self.schedule.period_end

        if required_temperature > current_temperature:

            self.warm_up_time_mins = int((required_temperature - current_temperature) / self.WARMUP_GRADIENT)
            warm_up_time = timedelta(minutes=self.warm_up_time_mins)
            warm_up_start_time = required_time - warm_up_time

            return datetime.now() >= warm_up_start_time

        else:
            return False

    @property
    def is_time_to_cool_down(self) -> bool:
        """
        Returns True if it is time to stop heating the house
        """
        required_temperature = self.schedule.inactive_period_minimum_temperature
        current_temperature = self.environment_sensor.internal_temperature
        required_time = self.schedule.period_end

        if current_temperature > required_temperature:

            self.cool_down_time_mins = int((current_temperature - required_temperature) / self.COOLDOWN_GRADIENT)
            cool_down_time = timedelta(minutes=self.cool_down_time_mins)
            cool_down_start_time = required_time - cool_down_time

            return datetime.now() >= cool_down_start_time

        else:
            return False

    @property
    def mode(self):
        pass
