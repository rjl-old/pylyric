from pylyric.schedule import Schedule
from pylyric.environment_sensor import EnvironmentSensor, Particle
from pylyric.heating_system import HeatingSystem, T6
from pylyric.house import House
from pylyric.utils import get_a_lyric_device
import datetime
import time

schedule = Schedule(
        active_period_start=datetime.time(8, 0),
        active_period_end=datetime.time(22, 0),
        active_period_minimum_temperature=20.0,
        inactive_period_minimum_temperature=18.0
)

honeywell = get_a_lyric_device()

environment_sensor: EnvironmentSensor = Particle()
heating_system: HeatingSystem = T6(honeywell)
house = House(environment_sensor=environment_sensor, heating_system=heating_system)

is_on = False
# main Loop
while True:
    current_temperature = house.environment_sensor.internal_temperature
    is_too_cold = current_temperature < schedule.minimum_temperature

    if schedule.is_active_period():

        if is_too_cold:
            house.heating_system.turn_on()
            is_on = True
        else:
            house.heating_system.turn_off()
            is_on = False

    else:

        if is_too_cold or house.is_time_to_start_heating():
            house.heating_system.turn_on()
            is_on = True
        else:
            house.heating_system.turn_off()
            is_on = False

    print(current_temperature)
    # -- write 'is_on' to influx here --
    time.sleep(10)
