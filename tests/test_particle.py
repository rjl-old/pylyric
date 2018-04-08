from pylyric.particle import Particle
import server.config as cfg


def test_internal_temperature():
    particle = Particle(auth_token=cfg.AUTH_TOKEN, device_id=cfg.DEVICE_ID)
    assert isinstance(particle.internal_temperture, float)
