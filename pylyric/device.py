#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
from typing import Dict

from pylyric.lyric import Lyric


class Device:
    """
    This class represents a Honeywell 'Lyric' T6 thermostat
    """

    def __init__(
            self,
            client: Lyric,
            location_id: int,
            device_id: int,
            changeable_values,
            allowed_modes,
            outdoor_humidity,
            outdoor_temperature,
            indoor_temperature,
            operation_status
    ):

        self.client = client
        self.location_id = location_id
        self.device_id = device_id
        self.changeable_values = changeable_values
        self.allowed_modes = allowed_modes
        self.outdoor_humidity = outdoor_humidity
        self.outdoor_temperature = outdoor_temperature
        self.indoor_temperature = indoor_temperature
        self.operation_status = operation_status

        self.last_update = datetime.datetime.now()

    @staticmethod
    def from_json(location_id: int, client: Lyric, data: Dict or str):
        if isinstance(data, str):
            data = json.loads(data)

        return Device(
            client,
            location_id,
            data['deviceID'],
            data['changeableValues'],
            data['allowedModes'],
            data['displayedOutdoorHumidity'],
            data['outdoorTemperature'],
            data['indoorTemperature'],
            data['operationStatus']['mode'],
        )

    def update(self) -> 'Device':
        """
        Gets the latest data for the device from the server.
        :return: The device for function chaining.
        """
        data = self.client.device(location_id=self.location_id, device_id=self.device_id)

        self.device_id = data['deviceID']
        self.changeable_values = data['changeableValues']
        self.allowed_modes = data['allowedModes']
        self.outdoor_humidity = int(data['displayedOutdoorHumidity'])
        self.outdoor_temperature = float(data['outdoorTemperature'])
        self.indoor_temperature = float(data['indoorTemperature'])
        self.operation_status = data['operationStatus']['mode']

        self.last_update = datetime.datetime.now()

        return self

    def change(self, **kwargs):
        """
        https://developer.honeywell.com/lyric/apis/post/devices/thermostats/%7BdeviceId%7D
        :return:
        """
        old_state = self.changeable_values
        new_state = old_state
        for k, v in kwargs.items():
            if k in new_state:
                new_state[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))

        self.client.change_device(location_id=self.location_id, device_id=self.device_id, **new_state)
        self.changeable_values = new_state
