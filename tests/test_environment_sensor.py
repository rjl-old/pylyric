from pylyric.environment_sensor import EnvironmentSensor, Particle
import server.config as cfg

environment_sensor: EnvironmentSensor = Particle(auth_token=cfg.AUTH_TOKEN, device_id=cfg.DEVICE_ID)


def test_initialise():
    assert isinstance(environment_sensor, Particle)


def test_internal_temperature():
    assert isinstance(environment_sensor.internal_temperature, float)
