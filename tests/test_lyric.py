from pylyric.lyric import Lyric, Device

lyric = Lyric()


class TestLyric:

    def test_devices(self):
        assert isinstance(lyric.devices[0], Device)


class TestDevice:

    def test_device_properties(self):
        device = lyric.devices[0]
        assert isinstance(device.device_id, str)
        assert isinstance(device.name, str)
        assert isinstance(device.indoor_temperature, float)
        assert isinstance(device.outdoor_temperature, float)
        assert isinstance(device.outdoor_humidity, int)
        assert isinstance(device.mode, str)
        assert isinstance(device.changeable_values, dict)

    def test_change(self):
        device = lyric.devices[0]

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
