from sanic import Sanic
from sanic import response

from pylyric.lyric import Lyric
from pylyric.device import Device
from pylyric.oauth2 import LyricClientCredentials
from server import config as cfg
from server.tasks import tasks, async_run_every

app = Sanic()

lcc = LyricClientCredentials(client_id=cfg.CLIENT_ID, client_secret=cfg.CLIENT_SECRET, access_token=cfg.ACCESS_TOKEN,
                             refresh_token=cfg.REFRESH_TOKEN)

lyric_client = Lyric(client_credentials_manager=lcc)

locationID = lyric_client.locations()[0]['locationID']
deviceID = lyric_client.locations()[0]['devices'][0]['deviceID']
device_dict = lyric_client.device(locationID, deviceID)

thermostat = Device(client=lyric_client, json=device_dict, location_id=locationID)


@app.route('/')
async def index(request):
    return response.text("Hello, World!")


@app.route('/server/v1.0/temperature/indoor', methods=['GET'])
async def get_indoor_temperature(request):
    return response.json({'indoorTemperature': thermostat.indoorTemperature})


@app.route('/server/v1.0/humidity/outdoor', methods=['GET'])
async def get_outdoor_humidity(request):
    return response.json({'outdoorHumidity': thermostat.outdoorHumidity})


@app.route('/server/v1.0/temperature/outdoor', methods=['GET'])
async def get_outdoor_temperature(request):
    return response.json({'outdoorTemperature': thermostat.outdoorTemperature})


@app.route('/server/v1.0/status', methods=['GET'])
async def get_operation_status(request):
    return response.json({'operationStatus': thermostat.operationStatus})


@app.route('/server/v1.0/mode', methods=['GET'])
async def get_mode(request):
    return response.json({'mode': thermostat.changeableValues['mode']})


@app.route('/lyric/api/v1.0/update', methods=['POST'])
async def post_update(request):
    thermostat.update()
    return response.json({'updated': thermostat.last_update})


@app.route('/lyric/api/v1.0/lastupdate', methods=['GET'])
async def get_last_update():
    return response.json({'lastUpdate': thermostat.last_update})


@async_run_every(seconds=600)
def update(device: Device):
    print("updating thermostat")
    device.update()


app.add_task(update(thermostat))

for task in tasks:
    app.add_task(task())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
