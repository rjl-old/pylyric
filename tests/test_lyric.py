from pylyric.lyric import Lyric
from pylyric.device import Device
from pylyric.oauth2 import LyricClientCredentials
import pylyric.config as cfg

lcc = LyricClientCredentials(
        client_id=cfg.CLIENT_ID,
        client_secret=cfg.CLIENT_SECRET,
        api_key=cfg.API_KEY,
        access_token=cfg.ACCESS_TOKEN,
        refresh_token=cfg.REFRESH_TOKEN,
        redirect_url=cfg.REDIRECT_URL
)

lyric = Lyric(client_credentials_manager=lcc)
lyric.trace_out = True
locationID = lyric.locations()[0]['locationID']
deviceID = lyric.locations()[0]['devices'][0]['deviceID']


def test_locations():
    assert isinstance(lyric.locations(), list)
    assert isinstance(lyric.locations()[0], dict)
    assert 'locationID' in lyric.locations()[0]


def test_devices():
    assert isinstance(lyric.devices(locationID), list)
    assert isinstance(lyric.devices(locationID)[0], Device)


def test_device():
    assert isinstance(lyric.device(locationID, deviceID), Device)
