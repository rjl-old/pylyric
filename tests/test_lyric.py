from pylyric.lyric import Lyric, Device

lyric = Lyric()


class TestLyric:

    def test_locations(self):
        assert isinstance(lyric.locations, list)
        first_location = lyric.locations[0]
        assert isinstance(first_location, dict)

    def test_devices(self):
        location_id = lyric.locations[0]['locationID']
        devices = lyric.devices(location_id=location_id)
        assert isinstance(devices, list)
        assert isinstance(devices[0], Device)p


class TestDevice:

    def test_device_properties(self):
        location_id = lyric.locations[0]['locationID']
        device = lyric.devices(location_id=location_id)[0]
        assert isinstance(device.device_id, str)
        assert isinstance(device.name, str)
        assert isinstance(device.indoor_temperature, float)
        assert isinstance(device.outdoor_temperature, float)
        assert isinstance(device.outdoor_humidity, int)
        assert isinstance(device.mode, str)
        assert isinstance(device.changeable_values, dict)

    def test_change(self):
        location_id = lyric.locations[0]['locationID']
        device = lyric.devices(location_id=location_id)[0]

        old_state = device.changeable_values
        old_mode = old_state['mode']

        if old_mode == "Off":
            new_mode = "Heat"
        else:
            new_mode = "Off"

        # change state and test
        device.change(mode=new_mode)
        assert device.changeable_values['mode'] == new_mode

        # return to original state
        device.change(mode=old_mode)
        assert device.changeable_values['mode'] == old_mode
