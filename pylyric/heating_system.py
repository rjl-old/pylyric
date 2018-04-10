from abc import abstractmethod, ABC


class HeatingSystem(ABC):
    """Base class for a heating system"""

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @property
    @abstractmethod
    def on(self):
        pass


class Device(HeatingSystem):
    """
    Implements heating system methods for a Honeywell Lyric T6
    """

    ON_TEMPERATURE = 25
    OFF_TEMPERATURE = 15

    def __init__(self, json, location_id, lyric):
        self.location_id = location_id
        self.device_id = json['deviceID']
        self.lyric = lyric
        self.name = json['name']

    @property
    def changeable_values(self):
        json = self._update()
        return json['changeableValues']

    @property
    def indoor_temperature(self):
        json = self._update()
        return float(json['indoorTemperature'])

    @property
    def outdoor_temperature(self):
        json = self._update()
        return float(json['outdoorTemperature'])

    @property
    def outdoor_humidity(self):
        json = self._update()
        return int(json['displayedOutdoorHumidity'])

    @property
    def mode(self):
        json = self._update()
        return json['operationStatus']['mode']

    def change(self, **kwargs):
        changeable_values = self.changeable_values
        for k, v in kwargs.items():
            if k in changeable_values:
                changeable_values[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))
        headers = {'Authorization': f'Bearer {self.lyric._get_access_token()}'}
        params = {'apikey': self.lyric.client_id, 'locationId': self.location_id}
        self.lyric.api.devices.thermostats(self.device_id).post(headers=headers, params=params, data=changeable_values)

    def _update(self):
        headers = {'Authorization': f'Bearer {self.lyric._get_access_token()}'}
        params = {'apikey': self.lyric.client_id, 'locationId': self.location_id}
        device_json = self.lyric.api.devices.thermostats(self.device_id).get(headers=headers, params=params)
        return device_json

    def __repr__(self):
        return f"DEVICE: {self.name}"

    def turn_on(self):
        self._on = True
        self.change(mode="Heat", heatSetpoint=self.ON_TEMPERATURE, thermostatSetpointStatus="PermanentHold")

    def turn_off(self):
        self._off = False
        self.change(mode="Off", heatSetpoint=self.OFF_TEMPERATURE, thermostatSetpointStatus="PermanentHold")

    @property
    def on(self) -> bool or None:
        return self._on if self._on else None
