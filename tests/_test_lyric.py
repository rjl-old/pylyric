from pylyric.location import Location
from pylyric.device import Device


def test_get_locations(lyric):
    first_location = lyric.get_locations()[0]
    assert isinstance(lyric.get_locations(), list)
    assert isinstance(first_location, Location)


def test_get_devices(lyric):
    first_location = lyric.get_locations()[0]
    assert isinstance(lyric.get_devices(first_location.location_id), list)
    assert isinstance(lyric.get_devices(first_location.location_id)[0], Device)


def test_device(lyric):
    first_location = lyric.get_locations()[0]
    first_device = lyric.get_devices(first_location.location_id)[0]
    assert isinstance(lyric.get_device(first_location.location_id, first_device.device_id), Device)


def test_change_device(lyric):
    location = lyric.get_locations()[0]
    device = lyric.get_devices(location.location_id)[0]

    # capture current state
    old_state = device.changeable_values
    old_mode = old_state['mode']

    if old_mode == "Off":
        new_mode = "Heat"
    else:
        new_mode = "Off"

    # change state and test
    print(" !! Changing device")
    device.change(mode=new_mode)
    new_state = lyric.get_device(location.location_id, device.device_id).changeable_values
    assert new_state['mode'] == new_mode

    # return to current state
    device.change(mode=old_mode)
    new_state = device.changeable_values
    assert new_state['mode'] == old_mode
