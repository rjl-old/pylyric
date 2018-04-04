#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Device:
    """
    This class represents a Honeywell 'Lyric' T6 thermostat
    """

    def __init__(self, client, json, locationID):
        """

        :param client: Lyric client
        :param json: json data returned from Lyric.device()
        """
        self.client = client

        self.locationID = locationID
        self.deviceID = None

        self.changeableValues = None
        self.allowedModes = None
        self.outdoorHumidity = None
        self.outdoorTemperature = None
        self.indoorTemperature = None
        self.operationStatus = None

        self._parse(json)

    def change(self, **kwargs):
        """
        https://developer.honeywell.com/lyric/apis/post/devices/thermostats/%7BdeviceId%7D
        :return:
        """
        url = "devices/thermostats/{}".format(self.deviceID)
        params = {"locationId": self.locationID}

        current_state = self.changeableValues
        for k, v in kwargs.items():
            if k in current_state:
                current_state[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))
        self.client._post(url, params, payload=current_state)
        self._update()

    def _update(self):
        url = "devices/thermostats/{}".format(self.deviceID)
        params = {"locationId": self.locationID}
        json = self.client._get(url, params)
        self._parse(json)

    def _parse(self, json):
        self.deviceID = json['deviceID']
        self.changeableValues = json['changeableValues']
        self.allowedModes = json['allowedModes']
        self.outdoorHumidity = json['displayedOutdoorHumidity']
        self.outdoorTemperature = json['outdoorTemperature']
        self.indoorTemperature = json['indoorTemperature']
        self.operationStatus = json['operationStatus']['mode']
