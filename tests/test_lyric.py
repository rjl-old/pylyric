from pylyric.lyric import ApiCredentials, Lyric, Device
import server.config as cfg

lyric = Lyric()


class TestApiCredentials:

    def test_refresh_token(self):
        """
        Tests the refresh token function to make sure
        a new api key is given from the server.
        """
        api = ApiCredentials(
                client_id=cfg.CLIENT_ID,
                client_secret=cfg.CLIENT_SECRET,
                access_token=cfg.ACCESS_TOKEN,
                refresh_token=cfg.REFRESH_TOKEN
        )

        token = api.access_token
        api._refresh_token()
        assert api.access_token != token


class TestLyric:

    def test_locations(self):
        assert isinstance(lyric.locations, list)
        first_location = lyric.locations[0]
        assert isinstance(first_location, dict)

    def test_devices(self):
        location_id = lyric.locations[0]['locationID']
        devices = lyric.devices(location_id=location_id)
        assert isinstance(devices, list)
        assert isinstance(devices[0], Device)

    def test_device(self):
        location_id = lyric.locations[0]['locationID']
        devices = lyric.devices(location_id=location_id)
        device_id = devices[0].device_id
        device = lyric.device(location_id=location_id, device_id=device_id)
        assert device.device_id == device_id


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

    def test_change_device(self):
        location_id = lyric.locations[0]['locationID']
        device = lyric.devices(location_id=location_id)[0]
        device_id = device.device_id
        old_state = device.changeable_values
        old_mode = old_state['mode']

        if old_mode == "Off":
            new_mode = "Heat"
        else:
            new_mode = "Off"

        # change state and test
        lyric.change_device(location_id=location_id, device_id=device_id, mode=new_mode)
        device = lyric.devices(location_id=location_id)[0]
        assert device.changeable_values['mode'] == new_mode

        # return to original state
        lyric.change_device(location_id=location_id, device_id=device_id, mode=old_mode)
        device = lyric.devices(location_id=location_id)[0]
        assert device.changeable_values['mode'] == old_mode
