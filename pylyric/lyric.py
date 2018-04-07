#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import List, Dict

import requests
from requests import HTTPError
from sanic.log import logger

from pylyric.device import Device
from pylyric.location import Location


class LyricException(Exception):
    def __init__(self, http_status, code, msg, headers=None):
        self.http_status = http_status
        self.code = code
        self.msg = msg
        # `headers` is used to support `Retry-After` in the event of a
        # 429 status code.
        if headers is None:
            headers = {}
        self.headers = headers

    def __str__(self):
        return 'http status: {0}, code:{1} - {2}'.format(
            self.http_status, self.code, self.msg)


class Lyric:
    """
    This class provides a client for managing Honeywell 'Lyric' devices.
    See: https://developer.honeywell.com/server-methods?field_smart_method_tags_tid=All
    """

    def __init__(self, credentials=None):
        """
        Create a Lyric API object
        :param credentials: An authorisation token (optional)
        """
        self.lyric_api = LyricApi(credentials)
        self._session = requests.Session()

    def get_locations(self) -> List[Location]:
        """
        https://developer.honeywell.com/lyric/apis/get/locations
        :return: list of dict
        """
        return [Location.from_json(self.lyric_api, loc) for loc in self.lyric_api.get('locations')]

    def get_location(self, location_id) -> Location:
        """

        :param location_id:
        :return:
        """
        pass

    def get_devices(self, location_id) -> List[Device]:
        """
        https://developer.honeywell.com/lyric/apis/get/devices
        :param location_id: int
        :return: list of dict of device properties
        """
        params = {"locationId": location_id}
        devices = self.lyric_api.get('devices', params)
        return [Device.from_json(location_id, self.lyric_api, device_data) for device_data in devices]

    def get_device(self, location_id, device_id, device_type=Device):
        """
        https://developer.honeywell.com/lyric/apis/get/devices/thermostats/%7BdeviceId%7D-0
        :param device_type:
        :param location_id:
        :param device_id:
        :return: dict of device properties
        """
        url = f"devices/thermostats/{device_id}"
        params = {"locationId": location_id}
        data = self.lyric_api.get(url, params)
        return device_type.from_json(location_id, self.lyric_api, data)


class LyricApi:
    """
    Encapsulates all the direct communication with the lyric api.
    """

    HONEYWELL_API = "https://api.honeywell.com/v2/"

    def __init__(self, client_credentials_manager=None):
        """
        Create a Lyric API object
        :param client_credentials_manager: An authorisation token (optional)
        """
        self.client_credentials_manager = client_credentials_manager
        self._session = requests.Session()

    def _get_auth_headers(self, headers: Dict or None = None) -> Dict[str, str]:
        """
        Creates auth headers for the current token.
        :param headers: An already existing headers object to add to.
        :return: A header dict with the correct auth.
        """
        if headers is None:
            return {'Authorization': f'Bearer {self.client_credentials_manager.get_access_token()}'}
        else:
            headers['Authorization'] = f'Bearer {self.client_credentials_manager.get_access_token()}'
            return headers

    def _internal_call(self, method, url, payload, params):
        args = dict(params=params)
        params['apikey'] = self.client_credentials_manager.client_id

        if not url.startswith(self.HONEYWELL_API):
            url = self.HONEYWELL_API + url

        headers = self._get_auth_headers({'Content-Type': 'application/json'})

        if payload:
            args["data"] = json.dumps(payload)

        request = self._session.request(method, url, headers=headers, **args)

        logger.debug(f"Making request to {url}")
        logger.debug(f" - headers: {headers}")
        logger.debug(f" - status : {request.status_code}")
        logger.debug(f" - method : {method}")
        if payload:
            logger.debug(" - payload:", json.dumps(payload))

        try:
            request.raise_for_status()
        except HTTPError:
            raise LyricException(request.status_code, -1, '%s:\n %s' % (request.url, request.json()),
                                 headers=request.headers)

        if request.text and len(request.text) > 0 and request.text != 'null':
            results = request.json()
            logger.debug(f" - return : {results}")
            return results
        else:
            return None

    def get(self, url, args=None, payload=None, **kwargs):
        """

        :param url:
        :param args:
        :param payload:
        :param kwargs:
        :return:
        """
        if args:
            kwargs.update(args)
        return self._internal_call('GET', url, payload, kwargs)

    def post(self, url, args=None, payload=None, **kwargs):
        """

        :param url:
        :param args:
        :param payload:
        :param kwargs:
        :return:
        """
        if args:
            kwargs.update(args)
        return self._internal_call('POST', url, payload, kwargs)
