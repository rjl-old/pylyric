#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
import pytest

# from pylyric.heating_system import T6
# from pylyric.oauth2 import ApiCredentials
# from pylyric.lyric import Lyric
# from server import config as config
#
# credentials = ApiCredentials(
#     client_id=config.CLIENT_ID,
#     client_secret=config.CLIENT_SECRET,
#     access_token=config.ACCESS_TOKEN,
#     refresh_token=config.REFRESH_TOKEN
# )
#
# lyric_client = Lyric(credentials=credentials)
#
# location_id = lyric_client.get_locations()[0].location_id
# thermostat = lyric_client.get_devices(location_id)[0]
#
#
# @pytest.fixture(scope="module")
# def lyric():
#     # lyric.trace_out = True
#     return lyric_client
#
#
# @pytest.fixture(scope="module")
# def device():
#     return thermostat
#
#
@pytest.fixture(scope="module")
def heating_system():
    return lyric_client.get_device("199754", "LCC-00D02DB6B4A8", T6)
