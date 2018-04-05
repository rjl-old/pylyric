#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
import pytest
from pylyric.oauth2 import LyricClientCredentials
from pylyric.lyric import Lyric
from pylyric.device import Device
import pylyric.config as cfg

lcc = LyricClientCredentials(client_id=cfg.CLIENT_ID, client_secret=cfg.CLIENT_SECRET, access_token=cfg.ACCESS_TOKEN,
                             refresh_token=cfg.REFRESH_TOKEN)
lyric_client = Lyric(client_credentials_manager=lcc)

locationID = lyric_client.locations()[0]['locationID']
deviceID = lyric_client.locations()[0]['devices'][0]['deviceID']
device_dict = lyric_client.device(locationID, deviceID)

thermostat = Device(client=lyric_client, json=device_dict, location_id=locationID)


@pytest.fixture(scope="module")
def lyric():
    # lyric.trace_out = True
    return lyric_client


@pytest.fixture(scope="module")
def device():
    return thermostat