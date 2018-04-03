from pylyric.lyric import Lyric
from pylyric.device import Device

client = Lyric()
deviceID = client.locations[0]['devices'][0]['deviceID']
d = client.device(deviceID)

def test_device():
    assert isinstance(d, Device)
    assert isinstance(d.deviceID, str)
    assert isinstance(d.outdoorHumidity, int)
    assert isinstance(d.indoorTemperature, float)
    assert isinstance(d.outdoorTemperature, float)
    assert isinstance(d.is_heating, bool)
    assert isinstance(d.changeableValues['coolSetpoint'], int)


def test_change():
    d.change()
