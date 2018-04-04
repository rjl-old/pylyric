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



