#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
import pytest
from pylyric.oauth2 import ApiCredentials
from pylyric.lyric import Lyric
from pylyric.device import Device
import server.config as cfg

lcc = ApiCredentials(client_id=cfg.CLIENT_ID, client_secret=cfg.CLIENT_SECRET, access_token=cfg.ACCESS_TOKEN,
                     refresh_token=cfg.REFRESH_TOKEN)
lyric_client = Lyric(credentials=lcc)

locationID = lyric_client.get_locations()[0].location_id
deviceID = lyric_client.get_locations()[0]._devices[0]['deviceID']
device_dict = lyric_client.get_thermostat(locationID, deviceID)

thermostat = Device(lyric_api=lyric_client, json=device_dict, location_id=locationID)


@pytest.fixture(scope="module")
def lyric():
    # lyric.trace_out = True
    return lyric_client


@pytest.fixture(scope="module")
def device():
    return thermostat