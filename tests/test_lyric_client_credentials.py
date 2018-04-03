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


def test_intialise():
    assert isinstance(lcc, LyricClientCredentials)


def test_refresh_token():
    t = lcc.access_token
    lcc._refresh()
    assert lcc.access_token != t


def test_is_token_expired():
    lcc._refresh()
    assert lcc._is_token_expired() == False
