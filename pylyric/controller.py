from pylyric.schedule import Schedule
from pylyric.lyric import Lyric
from pylyric.environment_sensor import EnvironmentSensor, Particle
from pylyric.heating_system import HeatingSystem, T6
from pylyric.oauth2 import ApiCredentials
from pylyric.house import House
from server import config as cfg

from datetime import time


schedule = Schedule(
        active_period_start=time(8,0),
        active_period_end=time(22,0),
        active_period_minimum_temperature=20.0,
        inactive_period_minimum_temperature=18.0
)

credentials = ApiCredentials(
        client_id=cfg.CLIENT_ID,
        client_secret=cfg.CLIENT_SECRET,
        access_token=cfg.ACCESS_TOKEN,
        refresh_token=cfg.REFRESH_TOKEN
)
lyric_client = Lyric(credentials=credentials)
location_id = lyric_client.get_locations()[0].location_id
honeywell = lyric_client.get_devices(location_id)[0]

environment_sensor: EnvironmentSensor = Particle()
heating_system: HeatingSystem = T6(honeywell)
house = House(environment_sensor=environment_sensor, heating_system=heating_system)

# main Loop
while True:
    current_temperature = house.environment_sensor.internal_temperature
    required_temperature = schedule.minimum_temperature
    is_too_cold = current_temperature < required_temperature

    if schedule.is_active_period():

        if is_too_cold:
            house.heating_system.turn_on()
        else:
            house.heating_system.turn_off()

    else:

        if is_too_cold or house.is_time_to_start_heating():
            house.heating_system.turn_on()
        else:
            house.heating_system.turn_off()
