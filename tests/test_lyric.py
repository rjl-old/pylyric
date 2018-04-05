def test_locations(lyric):
    assert isinstance(lyric.locations(), list)
    assert isinstance(lyric.locations()[0], dict)
    assert 'locationID' in lyric.locations()[0]


def test_devices(lyric):
    locationID = lyric.locations()[0]['locationID']
    assert isinstance(lyric.devices(locationID), list)
    assert isinstance(lyric.devices(locationID)[0], dict)


def test_device(lyric):
    locationID = lyric.locations()[0]['locationID']
    deviceID = lyric.locations()[0]['devices'][0]['deviceID']
    assert isinstance(lyric.device(locationID, deviceID), dict)


def test_change_device(lyric):
    locationID = lyric.locations()[0]['locationID']
    deviceID = lyric.locations()[0]['devices'][0]['deviceID']
    device = lyric.locations()[0]['devices'][0]

    # capture current state
    old_state = device['changeableValues']
    old_mode = old_state['mode']

    if old_mode == "Off":
        new_mode = "Heat"
    else:
        new_mode = "Off"

    # change state and test
    lyric.change_device(location_id=locationID, device_id=deviceID, mode=new_mode)
    new_state = lyric.device(locationID, deviceID)['changeableValues']
    assert new_state['mode'] == new_mode

    # return to current state
    # lyric.change_device(locationID=locationID, deviceID=deviceID, mode=old_mode)
    # new_state = lyric.device(locationID, deviceID)['changeableValues']
    # assert new_state['mode'] == old_mode
