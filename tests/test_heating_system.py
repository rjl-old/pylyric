from pylyric.heating_system import HeatingSystem, Lyric


def test_initialise(device):
    heating_system: HeatingSystem = Lyric(device)
    assert isinstance(heating_system, Lyric)


def test_turn_on(device):
    heating_system: HeatingSystem = Lyric(device)
    heating_system.turn_on()


def test_turn_off(device):
    heating_system: HeatingSystem = Lyric(device)
    heating_system.turn_off()
