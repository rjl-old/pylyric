from pylyric.environment_sensor import EnvironmentSensor

s = EnvironmentSensor()

def test_initialise():
    assert isinstance(s, EnvironmentSensor)

def test_internal_temperature():
    assert isinstance(s.internal_temperature, float)