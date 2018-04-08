from pylyric.heating_system import T6
import pytest


def test_initialise(heating_system):
    assert isinstance(heating_system, T6)


#
# NOTE: These tests change the heating system!
# TODO: Teardown to return system to previous state
#

@pytest.mark.skip(reason="Changes the heating system state!")
def test_turn_on(heating_system):
    heating_system.turn_on()


@pytest.mark.skip(reason="Changes the heating system state!")
def test_turn_off(heating_system):
    heating_system.turn_off()
