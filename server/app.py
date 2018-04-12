import datetime
from sanic import Sanic, response
from sanic.log import logger

from pylyric.environment_sensor import EnvironmentSensor
from pylyric.heating_system import HeatingSystem
from pylyric.house import House
from pylyric.influx import Influx
from pylyric.lyric import Lyric
from pylyric.photon import Photon
from pylyric.schedule import Schedule
from server.tasks import async_run_every, tasks

UPDATE_FREQUENCY = 300  # seconds
PHOTON_DEVICE_ID = "37002b001147343438323536"
ACTIVE_PERIOD_START = datetime.time(8, 0)
ACTIVE_PERIOD_END = datetime.time(22, 0)
ACTIVE_PERIOD_MINIMUM_TEMPERATURE = 20.0
INACTIVE_PERIOD_MINIMUM_TEMPERATURE = 18.0

schedule = Schedule(
        active_period_start=ACTIVE_PERIOD_START,
        active_period_end=ACTIVE_PERIOD_END,
        active_period_minimum_temperature=ACTIVE_PERIOD_MINIMUM_TEMPERATURE,
        inactive_period_minimum_temperature=INACTIVE_PERIOD_MINIMUM_TEMPERATURE
)

app = Sanic()

db = Influx(db_name="KW-HEATING")

photon = Photon(device_id=PHOTON_DEVICE_ID)
device = Lyric().devices[0]
environment_sensor: EnvironmentSensor = photon
heating_system: HeatingSystem = device
house = House(environment_sensor=environment_sensor, heating_system=heating_system)


@app.route('/')
async def index(request):
    return response.text("Hello, World!")


@async_run_every(seconds=UPDATE_FREQUENCY)
def check_schedule(house: House, schedule: Schedule):
    try:

        current_temperature = house.environment_sensor.internal_temperature

        if schedule.is_active_period():

            is_too_warm = current_temperature > schedule.active_period_minimum_temperature

            status = f"ACTIVE, T:{round(current_temperature,1)}, M:{round(schedule.minimum_temperature,1)}"

            if is_too_warm or house.is_time_to_cool_down(schedule):
                house.heating_system.turn_off()
                status += ", OFF"
                status += " (COOL-DOWN)" if house.is_time_to_cool_down(schedule) else ""
                db.write("controller",
                         heating=False,
                         cool_down=house.is_time_to_cool_down(schedule),
                         cool_down_time=house.cool_down_time_mins if house.is_time_to_cool_down(schedule) else 0,
                         warm_up=False,
                         warm_up_time=0)
            else:
                house.heating_system.turn_on()
                status += ", ON"
                db.write("controller",
                         heating=True,
                         cool_down=False,
                         cool_down_time=0,
                         warm_up=False,
                         warm_up_time=0)
        else:

            is_too_cold = current_temperature < schedule.inactive_period_minimum_temperature

            status = f"INACTIVE, T:{round(current_temperature,1)}, M:{round(schedule.minimum_temperature,1)}"

            if is_too_cold or house.is_time_to_warm_up(schedule):
                house.heating_system.turn_on()
                status += ", ON"
                status += " (WARM-UP)" if house.is_time_to_warm_up(schedule) else ""
                db.write("controller",
                         heating=True,
                         cool_down=False,
                         cool_down_time=0,
                         warm_up=house.is_time_to_warm_up(schedule),
                         warm_up_time=house.warm_up_time_mins if house.is_time_to_warm_up(schedule) else 0)
            else:
                house.heating_system.turn_off()
                status += ", OFF"
                db.write("controller",
                         heating=False,
                         cool_down=False,
                         cool_down_time=0,
                         warm_up=False,
                         warm_up_time=0)

        db.write("controller", minimum_temperature=schedule.minimum_temperature)
        logger.info(status)

    except:

        logger.error("Event loop failed. Skipping")

app.add_task(check_schedule(house, schedule))

for task in tasks:
    app.add_task(task())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
