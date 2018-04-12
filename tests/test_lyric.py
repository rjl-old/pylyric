from requests import Response
import pytest

from pylyric.lyric import Device, Lyric, LyricAPI

# These may change if physical device is reset
LOCATION_ID = 199754
DEVICE_ID = 'LCC-00D02DB6B4A8'

api = LyricAPI()
lyric = Lyric()
device = lyric.devices[0]
thermostat = api.get_thermostat(location_id=LOCATION_ID, device_id=DEVICE_ID)


class TestLyricAPI:

    def test_get_auth_token(self):
        assert isinstance(api._get_auth_token(), Response)

    def test_get_locations(self):
        keys = ['locationID', 'name', 'devices']
        locations = api.get_locations()
        assert isinstance(locations, Response)

        response_keys = list(locations.json()[0].keys())
        assert set(keys).issubset(response_keys)

    def test_get_thermostat(self):
        keys = ['indoorTemperature', 'outdoorTemperature', 'displayedOutdoorHumidity']
        assert isinstance(thermostat, Response)

        response_keys = list(thermostat.json().keys())
        assert set(keys).issubset(response_keys)

    def test_change_thermostat(self):
        old_mode = device.mode
        new_mode = "Heat" if old_mode == "Off" else "Off"
        api.change_thermostat(location_id=LOCATION_ID, device_id=DEVICE_ID, mode=new_mode)
        changed_mode = device.mode
        assert changed_mode == new_mode

        # change it back
        api.change_thermostat(location_id=LOCATION_ID, device_id=DEVICE_ID, mode=old_mode)


class TestLyric:

    def test_device_is_device(self):
        assert isinstance(lyric.devices[0], Device)


class TestDevice:

    def test_device_properties(self):
        assert isinstance(device.device_id, str)
        assert isinstance(device.location_id, int)
        assert isinstance(device.name, str)

    def test_mode(self):
        assert isinstance(device.mode, str)

    def test_operating_status(self):
        assert(device.operation_status in ['ON', 'OFF'])

    @pytest.mark.skip(reason="This physically turns the heating on. Supervise the test.")
    def test_turn_on(self):
        device.turn_on()

    @pytest.mark.skip(reason="This physically turns the heating off. Supervise the test.")
    def test_turn_off(self):
        device.turn_off()

    def test_internal_temperature(self):
        assert isinstance(device.internal_temperature, float)
        print(device.internal_temperature)
