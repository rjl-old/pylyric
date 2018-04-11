from requests import Response

from pylyric.lyric import Device, Lyric, LyricAPI

# api = LyricAPI()
lyric = Lyric()
device = lyric.devices[0]


class xTestLyricAPI:

    def test_get_auth_token(self):
        assert isinstance(api._get_auth_token(), Response)

    def test_get_locations(self):
        locations = api.get_locations()
        assert isinstance(locations, Response)


class xTestLyric:

    def test_devices(self):
        assert isinstance(lyric.devices[0], Device)


class TestDevice:

    def test_internal_temperature(self):
        assert isinstance(device.internal_temperature, float)
        print(device.internal_temperature)


    def xtest_device_properties(self):
        device = lyric.devices[0]
        assert isinstance(device.device_id, str)
        assert isinstance(device.name, str)
        assert isinstance(device.changeable_values, dict)
        assert isinstance(device.indoor_temperature, float)
        assert isinstance(device.outdoor_temperature, float)
        assert isinstance(device.outdoor_humidity, int)
        assert isinstance(device.mode, str)

    def xtest_change(self):
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
