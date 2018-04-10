import datetime

from sanic import Sanic, response
from sanic.log import logger

from pylyric.environment_sensor import EnvironmentSensor, Photon
from pylyric.heating_system import HeatingSystem
from pylyric.house import House
from pylyric.influx import Influx
from pylyric.lyric import Lyric
from pylyric.schedule import Schedule
from server import config as cfg
from server.tasks import async_run_every, tasks

UPDATE_FREQUENCY = 60  # seconds

app = Sanic()

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


@app.route('/')
async def index(request):
    return response.text("Hello, World!")


@app.route('/api/v1.0/temperature/indoor', methods=['GET'])
async def get_indoor_temperature(request):
    return response.json([{"temp": device.indoor_temperature} for device in devices])


@app.route('/api/v1.0/humidity/outdoor', methods=['GET'])
async def get_outdoor_humidity(request):
    return response.json([{'humidity': device.outdoor_humidity} for device in devices])


@app.route('/api/v1.0/temperature/outdoor', methods=['GET'])
async def get_outdoor_temperature(request):
    return response.json([{'outdoorTemperature': device.outdoor_temperature} for device in devices])


@app.route('/api/v1.0/status', methods=['GET'])
async def get_operation_status(request):
    return response.json([{'operationStatus': device.operation_status} for device in devices])


@app.route('/api/v1.0/mode', methods=['GET'])
async def get_mode(request):
    return response.json([{'mode': device.changeable_values['mode']} for device in devices])


@app.route('/api/v1.0/update', methods=['POST'])
async def post_update(request):
    for device in devices:
        device.update()
    return response.json([{'updated': device.last_update} for device in devices])


@app.route('/api/v1.0/update', methods=['GET'])
async def get_last_update(request):
    return response.json([{'lastUpdate': str(device.last_update)} for device in devices])


@async_run_every(seconds=UPDATE_FREQUENCY)
def check_schedule(house: House, schedule: Schedule):

    current_temperature = house.environment_sensor.internal_temperature

    if schedule.is_active_period():

        is_too_cold = current_temperature < schedule.active_period_minimum_temperature

        if (not is_too_cold) or house.is_time_to_cool_down(schedule):
            house.heating_system.turn_off()
            is_on = False

        else:
            house.heating_system.turn_on()
            is_on = True

    else: # is inactive period

        is_too_cold = current_temperature < schedule.inactive_period_minimum_temperature

        if is_too_cold or house.is_time_to_warm_up(schedule):
            house.heating_system.turn_on()
            is_on = True

        else:
            house.heating_system.turn_off()
            is_on = False

    status = f"T:{round(current_temperature,1)}, M:{round(schedule.minimum_temperature,1)}"
    if house.heating_system.is_on:
        status += ", ON"
    else:
        status += ", OFF"

    if house.is_time_to_warm_up(schedule):
        status += ", PRE-WARM"
        db.write("controller", pre_warm=True)

    elif house.is_time_to_cool_down(schedule):
        status += ", COOL-DOWN"
        db.write("controller", cool_down=True)

    logger.info(status)
    db.write("controller", heating=heating_system.is_on)


app.add_task(check_schedule(house, schedule))

for task in tasks:
    app.add_task(task())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
