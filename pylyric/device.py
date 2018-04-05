#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime



class Device:
    """
    This class represents a Honeywell 'Lyric' T6 thermostat
    """

    def __init__(self, client, json, location_id):
        """

        :param client: Lyric client
        :param json: json data returned from Lyric.device()
        """
        self.client = client

        self.locationID = location_id
        self.deviceID = None

        self.changeableValues = None
        self.allowedModes = None
        self.outdoorHumidity = None
        self.outdoorTemperature = None
        self.indoorTemperature = None
        self.operationStatus = None

        self.last_update = None

        self._parse(json)

    def update(self):
        json = self.client.device(location_id=self.locationID, device_id=self.deviceID)
        self._parse(json)

    def change(self, **kwargs):
        """
        https://developer.honeywell.com/lyric/apis/post/devices/thermostats/%7BdeviceId%7D
        :return:
        """
        old_state = self.changeableValues
        new_state = old_state
        for k, v in kwargs.items():
            if k in new_state:
                new_state[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))

        self.client.change_device(location_id=self.locationID, device_id=self.deviceID, **new_state)
        self.changeableValues = new_state

    def _parse(self, json):
        self.deviceID = json['deviceID']
        self.changeableValues = json['changeableValues']
        self.allowedModes = json['allowedModes']
        self.outdoorHumidity = int(json['displayedOutdoorHumidity'])
        self.outdoorTemperature = float(json['outdoorTemperature'])
        self.indoorTemperature = float(json['indoorTemperature'])
        self.operationStatus = json['operationStatus']['mode']

        self.last_update = datetime.datetime.now()
