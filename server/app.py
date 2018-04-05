from typing import List

from sanic import Sanic
from sanic import response
from sanic.log import logger

from pylyric.lyric import Lyric
from pylyric.device import Device
from pylyric.oauth2 import ApiCredentials
from server import config as cfg
from server.tasks import tasks, async_run_every

app = Sanic()

credentials = ApiCredentials(
    client_id=cfg.CLIENT_ID,
    client_secret=cfg.CLIENT_SECRET,
    access_token=cfg.ACCESS_TOKEN,
    refresh_token=cfg.REFRESH_TOKEN
)

lyric_client = Lyric(credentials=credentials)
devices = lyric_client.get_locations()[0].get_devices()


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


@async_run_every(seconds=600)
def update(devices: List[Device] or Device):
    logger.info("Updating Devices")
    if isinstance(devices, list):
        for device in devices:
            device.update()
    else:
        devices.update()


app.add_task(update(devices))

for task in tasks:
    app.add_task(task())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
