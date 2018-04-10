from pylyric.lyric import Lyric
from pylyric.schedule import Schedule
from pylyric.environment_sensor import EnvironmentSensor, Photon
from pylyric.heating_system import HeatingSystem
from pylyric.house import House
import datetime
import time
from sanic.log import logger
from pylyric.influx import Influx
import server.config as cfg

UPDATE_FREQUENCY = 60 # seconds

db = Influx(db_name="test")

schedule = Schedule(
        active_period_start=datetime.time(8, 0),
        active_period_end=datetime.time(22, 0),
        active_period_minimum_temperature=20.0,
        inactive_period_minimum_temperature=18.0
)

photon = Photon(auth_token=cfg.AUTH_TOKEN, device_id=cfg.DEVICE_ID)
device = Lyric().devices[0]

environment_sensor: EnvironmentSensor = photon
heating_system: HeatingSystem = device

house = House(environment_sensor=environment_sensor, heating_system=heating_system)


# main Loop
while True:
    old_is_on = None

    current_temperature = house.environment_sensor.internal_temperature
    is_too_cold = current_temperature < schedule.minimum_temperature

    if schedule.is_active_period():

        if (not is_too_cold) or house.is_time_to_stop_heating(
                required_temperature=schedule.minimum_temperature,
                current_temperature=current_temperature,
                required_time=schedule.period_end):

            house.heating_system.turn_off()
            is_on = False
        else:
            house.heating_system.turn_on()
            is_on = True

    else:

        if is_too_cold or house.is_time_to_start_heating(
                required_temperature=schedule.minimum_temperature,
                current_temperature=current_temperature,
                required_time=schedule.period_end):

            house.heating_system.turn_on()
            is_on = True
        else:
            house.heating_system.turn_off()
            is_on = False

    if is_on != old_is_on:
        if is_on:
            logger.info("Heating on")
        else:
            logger.info("Heating off")
    old_is_on = is_on
    print(current_temperature)

    db.write("controller", heating=heating_system.is_on)

    time.sleep(UPDATE_FREQUENCY)
