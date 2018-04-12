from datetime import datetime

import pytest
from requests import Response

from pylyric.photon import ParticleAPI, Photon

PHOTON_DEVICE_ID = "37002b001147343438323536"

api = ParticleAPI()
photon = Photon(device_id=PHOTON_DEVICE_ID)


class TestParticleAPI:

    def test_get_device_information(self):
        assert isinstance(api.get_device_information(device_id=PHOTON_DEVICE_ID), Response)

    def test_get_variable(self):
        # Assumes Photon firmware presents 'temperature' variable: modify as required
        assert isinstance(api.get_variable(device_id=PHOTON_DEVICE_ID, variable_name='temperature'), Response)

    def test_get_missing_variable_raises_exception(self):
        with pytest.raises(Exception):
            api.get_variable(device_id=PHOTON_DEVICE_ID, variable_name='xxx')


class TestPhoton:

    def test_name(self):
        assert isinstance(photon.name, str)

    def test_connected(self):
        assert isinstance(photon.connected, bool)

    def test_last_heard(self):
        assert isinstance(photon.last_heard, datetime)

    def test_variables(self):
        assert isinstance(photon.variables, dict)

    def test_internal_temperature(self):
        assert isinstance(photon.internal_temperature, float)

    def test_get_missing_variable_raises_exception(self):
        bad_photon = Photon(device_id=PHOTON_DEVICE_ID)
        bad_photon.variables = []
        with pytest.raises(Exception):
            temp = bad_photon.internal_temperature
