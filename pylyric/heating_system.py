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
    def is_on(self):
        pass


class Device(HeatingSystem):
    """
    Implements heating system methods for a Honeywell Lyric T6
    """

    ON_TEMPERATURE = 25  # degC - arbitrary, just need 'hot'
    OFF_TEMPERATURE = 15  # degC - arbitrary, just need 'cold'

    def __init__(self, json, location_id, lyric):
        self.device_id = json['deviceID']
        self.name = json['name']
        self.location_id = location_id
        self.lyric = lyric
        self._on = None

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

    @property
    def is_on(self) -> bool:
        return True if self._on else False

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

    def turn_on(self):
        self._on = True
        self.change(mode="Heat", heatSetpoint=self.ON_TEMPERATURE, thermostatSetpointStatus="PermanentHold")

    def turn_off(self):
        self._on = False
        self.change(mode="Off", heatSetpoint=self.OFF_TEMPERATURE, thermostatSetpointStatus="PermanentHold")

    def _update(self):
        headers = {'Authorization': f'Bearer {self.lyric._get_access_token()}'}
        params = {'apikey': self.lyric.client_id, 'locationId': self.location_id}
        device_json = self.lyric.api.devices.thermostats(self.device_id).get(headers=headers, params=params)
        return device_json

    def __repr__(self):
        return f"DEVICE: {self.name}"
