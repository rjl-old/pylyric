from pylyric.photon import Photon
from datetime import datetime

PHOTON_DEVICE_ID = "37002b001147343438323536"

photon = Photon(device_id=PHOTON_DEVICE_ID)


def test_name():
    assert isinstance(photon.name, str)


def test_connected():
    assert isinstance(photon.connected, bool)


def test_last_heard():
    assert isinstance(photon.last_heard, datetime)


def test_variables():
    assert isinstance(photon.variables, dict)


def test_internal_temperature():
    assert isinstance(photon.internal_temperature, float)
    print(photon.internal_temperature)
