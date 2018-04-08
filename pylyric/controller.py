from pylyric.schedule import Schedule
from pylyric.environment_sensor import EnvironmentSensor
from pylyric.heating_system import HeatingSystem, T6
from pylyric.house import House
from pylyric.utils import get_the_t6, get_the_photon
import datetime
import time
from sanic.log import logger
from pylyric.influx import Influx

db = Influx(db_name="test")

schedule = Schedule(
        active_period_start=datetime.time(8, 0),
        active_period_end=datetime.time(22, 0),
        active_period_minimum_temperature=20.0,
        inactive_period_minimum_temperature=18.0
)

environment_sensor: EnvironmentSensor = get_the_photon()
honeywell = get_the_t6()
heating_system: HeatingSystem = T6(honeywell)
house = House(environment_sensor=environment_sensor, heating_system=heating_system)

old_is_on = False
is_on = False

# main Loop
while True:
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

    db.write("controller", heating=is_on)

    time.sleep(10)
