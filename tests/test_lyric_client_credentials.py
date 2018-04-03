from pylyric.oauth2 import LyricClientCredentials
import datetime

data = {
    "client": {
        "client_id": "2IvMPqBmBBDhl3vBWVbCs4IvqjfQ9AUZ",
        "client_secret": "lmVks7zDAdyoRQOT",
        "api_key": "v4M5vCGGt0F6tMwxwb2ac5UGENegSS4H",
        "redirect_url": "kingswood"
    },
    "tokens": {
        "access_token": "AZJyWOGjxUVtpGQ2w7jNA9EdWu8O",
        "refresh_token": "G84Tia8JeST2ELVBqWQWRdZ4cQuqWKZM"
    }
}

lcc = LyricClientCredentials(
        client_id=data['client']['client_id'],
        client_secret=data['client']['client_secret'],
        api_key=data['client']['api_key'],
        access_token=data['tokens']['access_token'],
        refresh_token=data['tokens']['refresh_token'],
        redirect_url=data['client']['redirect_url']
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
