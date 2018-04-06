from flask import Flask, jsonify
from pylyric.lyric import Lyric
from pylyric.device import Device
from pylyric.oauth2 import LyricClientCredentials
import pylyric.config as cfg

app = Flask(__name__)

lcc = LyricClientCredentials(
        client_id=cfg.CLIENT_ID,
        client_secret=cfg.CLIENT_SECRET,
        api_key=cfg.API_KEY,
        access_token=cfg.ACCESS_TOKEN,
        refresh_token=cfg.REFRESH_TOKEN,
        redirect_url=cfg.REDIRECT_URL
)
lyric_client = Lyric(client_credentials_manager=lcc)

locationID = lyric_client.locations()[0]['locationID']
deviceID = lyric_client.locations()[0]['devices'][0]['deviceID']
device_dict = lyric_client.device(locationID, deviceID)

thermostat = Device(client=lyric_client, json=device_dict, locationID=locationID)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/lyric/api/v1.0/indoortemperature', methods=['GET'])
def get_indoortemperature():
    return jsonify({'indoorTemperature': thermostat.indoorTemperature})


@app.route('/lyric/api/v1.0/outdoorhumidity', methods=['GET'])
def get_outdoorHumidity():
    return jsonify({'outdoorHumidity': thermostat.outdoorHumidity})


@app.route('/lyric/api/v1.0/outdoortemperature', methods=['GET'])
def get_outdoorTemperature():
    return jsonify({'outdoorTemperature': thermostat.outdoorTemperature})


@app.route('/lyric/api/v1.0/operationstatus', methods=['GET'])
def get_operationStatus():
    return jsonify({'operationStatus': thermostat.operationStatus})


@app.route('/lyric/api/v1.0/mode', methods=['GET'])
def get_mode():
    return jsonify({'mode': thermostat.changeableValues['mode']})


if __name__ == '__main__':
    app.run(debug=True)
