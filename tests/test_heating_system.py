from pylyric.heating_system import HeatingSystem, T6
import pytest

def test_initialise(device):
    heating_system: HeatingSystem = T6(device)
    assert isinstance(heating_system, T6)

#
# NOTE: These tests change the heating system!
# TODO: Teardown to return system to previous state
#

@pytest.mark.skip(reason="Changes the heating system state!")
def test_turn_on(device):
    heating_system: HeatingSystem = Lyric(device)
    heating_system.turn_on()

@pytest.mark.skip(reason="Changes the heating system state!")
def test_turn_off(device):
    heating_system: HeatingSystem = Lyric(device)
    heating_system.turn_off()
