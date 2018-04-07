def test_allowed_modes(device):
    assert isinstance(device.allowedModes, list)


def test_change(device):
    # GIVEN a device
    # WHEN I change a changeable value
    # THEN the device changes

    # capture current state
    old_state = device.changeable_values
    old_mode = old_state['mode']

    if old_mode == "Off":
        new_mode = "Heat"
    else:
        new_mode = "Off"

    # change state and test
    device.change(mode=new_mode)
    assert device.changeable_values['mode'] == new_mode

    # return to current state
    device.change(mode=old_mode)
    assert device.changeable_values['mode'] == old_mode
