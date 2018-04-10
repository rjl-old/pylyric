from pylyric.environment_sensor import EnvironmentSensor, Photon
from pylyric.particle import Particle
import server.config as cfg

particle = Particle(auth_token=cfg.AUTH_TOKEN, device_id=cfg.DEVICE_ID)

environment_sensor: EnvironmentSensor = Photon(particle)


def test_initialise():
    assert isinstance(environment_sensor, Particle)


def test_internal_temperature():
    assert isinstance(environment_sensor.internal_temperature, float)
