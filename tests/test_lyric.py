from pylyric.lyric import Lyric

def test_initialisation():
    client = Lyric()
    assert client.client_id == "2IvMPqBmBBDhl3vBWVbCs4IvqjfQ9AUZ"
    assert client.client_secret == "lmVks7zDAdyoRQOT"
    assert client.client_auth == b"Mkl2TVBxQm1CQkRobDN2QldWYkNzNEl2cWpmUTlBVVo6bG1Wa3M3ekRBZHlvUlFPVA=="
    assert client.api_key == "v4M5vCGGt0F6tMwxwb2ac5UGENegSS4H"
    assert client.redirect_url == "kingswood"
    assert client.access_token == "AZJyWOGjxUVtpGQ2w7jNA9EdWu8O"
    assert client.refresh_token == "G84Tia8JeST2ELVBqWQWRdZ4cQuqWKZM"


# def test_refresh_token():
#     client = Lyric()
#     t = client.access_token
#     r = client.refresh()
#     assert client.access_token != t
#
#
# def test_get_location():
#     l = Lyric()
#     assert l.locations[0]['locationID'] == 199754