from pylyric.oauth2 import ApiCredentials
import server.config as cfg


def test_refresh_token():
    """
    Tests the refresh token function to make sure
    a new api key is given from the server.
    """
    lcc = ApiCredentials(
        client_id=cfg.CLIENT_ID,
        client_secret=cfg.CLIENT_SECRET,
        access_token=cfg.ACCESS_TOKEN,
        refresh_token=cfg.REFRESH_TOKEN
    )

    token = lcc.access_token
    lcc._refresh_token()
    assert lcc.access_token != token
