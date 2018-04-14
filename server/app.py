from dateutil.parser import parse
from sanic import Sanic, response
from sanic.log import logger

from pylyric.controller import Controller
from pylyric.environment_sensor import EnvironmentSensor
from pylyric.heating_system import HeatingSystem
from pylyric.house import House
from pylyric.influx import Influx
from pylyric.lyric import Lyric
from pylyric.photon import Photon
from pylyric.schedule import Schedule
from pylyric.utils import record
from server.tasks import async_run_every, tasks

app = Sanic()

UPDATE_FREQUENCY = 10  # seconds

ACTIVE_TEMPERATURE = 21.0
INACTIVE_TEMPERATURE = 19.0
ACTIVE_PERIOD_START = parse("07:00").time()
INACTIVE_PERIOD_START = parse("21:00").time()
schedule = Schedule(
        active_temperature=ACTIVE_TEMPERATURE,
        inactive_temperature=INACTIVE_TEMPERATURE,
        active_period_start=ACTIVE_PERIOD_START,
        inactive_period_start=INACTIVE_PERIOD_START,
)

INFLUX_DATABASE_NAME = "test"
db = Influx(db_name=INFLUX_DATABASE_NAME)

PHOTON_DEVICE_ID = "37002b001147343438323536"
photon = Photon(device_id=PHOTON_DEVICE_ID)

device = Lyric().devices[0]

environment_sensor: EnvironmentSensor = photon
heating_system: HeatingSystem = device

house = House(environment_sensor=environment_sensor, heating_system=heating_system)

controller = Controller(house=house, schedule=schedule)


@app.route('/')
async def index(request):
    return response.text("Hello, World!")


@async_run_every(seconds=UPDATE_FREQUENCY)
def check_schedule(house: House, schedule: Schedule):
    try:
        controller.set_heating()
        logger.info(controller.status)

        record(db, controller)

    except Exception as e:
        logger.error(f"Event loop failed: {e}")


app.add_task(check_schedule(house, schedule))

for task in tasks:
    app.add_task(task())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
