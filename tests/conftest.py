#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
import pytest

from pylyric.oauth2 import ApiCredentials
from pylyric.lyric import Lyric
from pylyric.device import Device
from server import config as cfg

credentials = ApiCredentials(
    client_id=cfg.CLIENT_ID,
    client_secret=cfg.CLIENT_SECRET,
    access_token=cfg.ACCESS_TOKEN,
    refresh_token=cfg.REFRESH_TOKEN
)

lyric_client = Lyric(credentials=credentials)

locationID = lyric_client.get_locations()[0].location_id
# deviceID = lyric_client.locations()[0]['devices'][0]['deviceID']
# device_dict = lyric_client.device(locationID, deviceID)
#
# thermostat = Device(client=lyric_client, json=device_dict, locationID=locationID)


@pytest.fixture(scope="module")
def lyric():
    # lyric.trace_out = True
    return lyric_client