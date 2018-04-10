from pylyric.lyric import Lyric
from pylyric.heating_system import HeatingSystem

lyric = Lyric()
heating_system: HeatingSystem = lyric.devices[0]
#
def test_initialise():
    assert isinstance(heating_system, HeatingSystem)


#
# NOTE: These tests change the heating system!
# TODO: Teardown to return system to previous state
#

# @pytest.mark.skip(reason="Changes the heating system state!")
# def test_turn_on(heating_system):
#     heating_system.turn_on()
#
#
# @pytest.mark.skip(reason="Changes the heating system state!")
# def test_turn_off(heating_system):
#     heating_system.turn_off()
