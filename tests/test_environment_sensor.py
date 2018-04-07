from pylyric.environment_sensor import EnvironmentSensor, Particle

environment_sensor: EnvironmentSensor = Particle()


def test_initialise():
    assert isinstance(environment_sensor, Particle)


def test_internal_temperature():
    assert isinstance(environment_sensor.internal_temperature, float)
