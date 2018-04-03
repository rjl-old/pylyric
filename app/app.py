from flask import Flask, jsonify
from pylyric.lyric import Lyric
from pylyric.device import Device

client = Lyric()
deviceID = client.locations[0]['devices'][0]['deviceID']
d = client.device(deviceID)

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/lyric/api/v1.0/indoortemperature', methods=['GET'])
def get_indoortemperature():
    return jsonify({'indoorTemperature': d.indoorTemperature})


if __name__ == '__main__':
    app.run(debug=True)
