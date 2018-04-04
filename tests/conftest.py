#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
import pytest
from pylyric.lyric import Lyric
from pylyric.oauth2 import LyricClientCredentials
import pylyric.config as cfg

@pytest.fixture(scope="module")
def lyric():
    lcc = LyricClientCredentials(
            client_id=cfg.CLIENT_ID,
            client_secret=cfg.CLIENT_SECRET,
            api_key=cfg.API_KEY,
            access_token=cfg.ACCESS_TOKEN,
            refresh_token=cfg.REFRESH_TOKEN,
            redirect_url=cfg.REDIRECT_URL
    )
    lyric = Lyric(client_credentials_manager=lcc)
    # lyric.trace_out = True
    return lyric