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

    def __init__(self, heating_system: HeatingSystem = None, environment_sensor: EnvironmentSensor = None):
        self.heating_system = heating_system
        self.environment_sensor = environment_sensor


