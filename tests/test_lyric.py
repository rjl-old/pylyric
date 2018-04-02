from pylyric.lyric import Lyric
import pytest

client = Lyric()

def test_initialisation():
    # client = Lyric()
    assert client.client_id == "2IvMPqBmBBDhl3vBWVbCs4IvqjfQ9AUZ"
    assert client.client_secret == "lmVks7zDAdyoRQOT"
    assert client.api_key == "v4M5vCGGt0F6tMwxwb2ac5UGENegSS4H"
    assert client.redirect_url == "kingswood"
    # assert client.access_token == "AZJyWOGjxUVtpGQ2w7jNA9EdWu8O"
    assert client.refresh_token == "G84Tia8JeST2ELVBqWQWRdZ4cQuqWKZM"


def test_refresh_token():
    t = client.access_token
    client.refresh_tokens()
    assert client.access_token != t


def test_get_location():
    assert isinstance(client.locations[0]['locationID'], int)


def test_get_devices():
    assert isinstance(client.devices(locationID=199754)[0]['deviceID'], str)