from pylyric.lyric import Lyric
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
lyric.trace_out = False
locationID = lyric.locations()[0]['locationID']
deviceID = lyric.locations()[0]['devices'][0]['deviceID']


def test_locations():
    assert isinstance(lyric.locations(), list)
    assert isinstance(lyric.locations()[0], dict)
    assert 'locationID' in lyric.locations()[0]


def test_devices():
    assert isinstance(lyric.devices(locationID), list)
    assert isinstance(lyric.devices(locationID)[0], dict)


def test_device():
    assert isinstance(lyric.device(locationID, deviceID), dict)


def test_change_device():
    current_state = lyric.device(locationID, deviceID)['changeableValues']
    old_mode = current_state['mode']
    if old_mode == "Off":
        new_mode = "Heat"
    else:
        new_mode = "Off"

    lyric.change_device(locationID, deviceID, mode=new_mode)
    current_state = lyric.device(locationID, deviceID)['changeableValues']
    assert current_state['mode'] == new_mode

    lyric.change_device(locationID, deviceID, mode=old_mode)
    current_state = lyric.device(locationID, deviceID)['changeableValues']
    assert current_state['mode'] == old_mode
