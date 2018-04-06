from pylyric.boiler import Boiler

b = Boiler()

def test_initialise():
    assert isinstance(b, Boiler)

def test_turn_on():
    b.turn_on()