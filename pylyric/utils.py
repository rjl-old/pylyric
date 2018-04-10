import base64
import json
import os

from server import config as cfg
from pylyric.oauth2 import ApiCredentials
from pylyric.lyric import Lyric
from pylyric.particle import Particle


def print_authorisation():
    """prints the base64 encoded result of id:secret
       -> G84Tia8JeST2ELVBqWQWRdZ4cQuqWKZM
    """
    config_file = os.path.join((os.path.abspath(os.path.dirname(__file__))), "auth.json")
    with open(config_file) as json_file:
        config_data = json.load(json_file)

    string = "{}:{}".format(config_data['client']['client_id'], config_data['client']['client_secret'])
    print(base64.b64encode(string.encode('utf-8')))