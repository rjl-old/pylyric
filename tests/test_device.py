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
locationID = lyric.locations()[0]['locationID']
deviceID = lyric.locations()[0]['devices'][0]['deviceID']
device = lyric.device(locationID, deviceID)


def test_allowed_modes():
    assert isinstance(device.allowedModes, list)


def test_change_device():
    current_state = device.changeableValues
    old_mode = current_state['mode']

    if old_mode == "Off":
        new_mode = "Heat"
    else:
        new_mode = "Off"

    device.change(mode=new_mode)
    assert device.changeableValues['mode'] == new_mode

    device.change(mode=old_mode)
    assert device.changeableValues['mode'] == old_mode
