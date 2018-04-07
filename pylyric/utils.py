import base64
import json
import os

from server import config as cfg
from pylyric.oauth2 import ApiCredentials
from pylyric.lyric import Lyric


def print_authorisation():
    """prints the base64 encoded result of id:secret
       -> G84Tia8JeST2ELVBqWQWRdZ4cQuqWKZM
    """
    config_file = os.path.join((os.path.abspath(os.path.dirname(__file__))), "auth.json")
    with open(config_file) as json_file:
        config_data = json.load(json_file)

    string = "{}:{}".format(config_data['client']['client_id'], config_data['client']['client_secret'])
    print(base64.b64encode(string.encode('utf-8')))


def get_a_lyric_device():
    credentials = ApiCredentials(
        client_id=cfg.CLIENT_ID,
        client_secret=cfg.CLIENT_SECRET,
        access_token=cfg.ACCESS_TOKEN,
        refresh_token=cfg.REFRESH_TOKEN
    )
    lyric_client = Lyric(credentials=credentials)
    location_id = lyric_client.get_locations()[0].location_id
    return lyric_client.get_devices(location_id)[0]
