from pylyric.boiler import Boiler
from pylyric.lyric import Lyric
from pylyric.oauth2 import ApiCredentials
from server import config

LOCATION_ID = "199754"
DEVICE_ID = "LCC-00D02DB6B4A8"

credentials = ApiCredentials(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    access_token=config.ACCESS_TOKEN,
    refresh_token=config.REFRESH_TOKEN
)


lyric_client = Lyric(credentials=credentials)
boiler = lyric_client.get_device(LOCATION_ID, DEVICE_ID, Boiler)


def test_initialise():
    assert isinstance(boiler, Boiler)


def test_turn_on():
    boiler.turn_on()
