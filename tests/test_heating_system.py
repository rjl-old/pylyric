from pylyric.heating_system import HeatingSystem

h = HeatingSystem()

def test_initialise():
    assert isinstance(h, HeatingSystem)

def test_turn_on():
    h.turn_on()