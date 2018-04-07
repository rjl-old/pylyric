from pylyric.environment_sensor import EnvironmentSensor, Particle

particle: EnvironmentSensor = Particle()

def test_initialise():
    assert isinstance(particle, Particle)

def test_internal_temperature():
    assert isinstance(particle.internal_temperature, float)