#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import requests
from requests import HTTPError


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

    trace_out = False

    def __init__(self, client_credentials_manager=None):
        """
        Create a Lyric API object
        :param client_credentials_manager: An authorisation token (optional)
        """
        self.prefix = "https://api.honeywell.com/v2/"
        self.client_credentials_manager = client_credentials_manager
        self._session = requests.Session()

    def _auth_headers(self):
        if self.client_credentials_manager:
            token = self.client_credentials_manager.get_access_token()
            return {'Authorization': 'Bearer {0}'.format(token)}
        else:
            return {}

    def _internal_call(self, method, url, payload, params):
        args = dict(params=params)
        params['apikey'] = self.client_credentials_manager.client_id

        if not url.startswith('http'):
            url = self.prefix + url

        headers = self._auth_headers()
        headers['Content-Type'] = 'application/json'

        if payload:
            args["data"] = json.dumps(payload)

        if self.trace_out:
            print()
            print('>>', url)

        request = self._session.request(method, url, headers=headers, **args)

        if self.trace_out:
            print('>> headers', headers)
            print('>> http status', request.status_code)
            print('>>', method, request.url)
            if payload:
                print(">> DATA", json.dumps(payload))
        try:
            request.raise_for_status()
        except HTTPError:
            raise LyricException(request.status_code, -1, '%s:\n %s' % (request.url, request.json()), headers=request.headers)
        finally:
            request.connection.close()

        if request.text and len(request.text) > 0 and request.text != 'null':
            results = request.json()
            if self.trace_out:  # pragma: no cover
                print('>> RESP', results)
                print()
            return results
        else:
            return None

    def _get(self, url, args=None, payload=None, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call('GET', url, payload, kwargs)

    def _post(self, url, args=None, payload=None, **kwargs):
        if args:
            kwargs.update(args)
        return self._internal_call('POST', url, payload, kwargs)

    def locations(self):
        """
        https://developer.honeywell.com/lyric/apis/get/locations
        :return: list of dict
        """
        return self._get('locations')

    def devices(self, location_id):
        """
        https://developer.honeywell.com/lyric/apis/get/devices
        :param location_id: int
        :return: list of dict of device properties
        """
        params = {"locationId": location_id}
        data = self._get('devices', params)
        return data

    def device(self, location_id, device_id):
        """
        https://developer.honeywell.com/lyric/apis/get/devices/thermostats/%7BdeviceId%7D-0
        :param location_id:
        :param device_id:
        :return: dict of device properties
        """
        url = "devices/thermostats/{}".format(device_id)
        params = {"locationId": location_id}
        data = self._get(url, params)
        return data

    def change_device(self, location_id, device_id, **kwargs):
        """
        https://developer.honeywell.com/lyric/apis/post/devices/thermostats/%7BdeviceId%7D
        :param location_id: int
        :param device_id: int
        :return:
        """
        url = "devices/thermostats/{}".format(device_id)
        params = {"locationId": location_id}

        current_state = self.device(location_id, device_id)['changeableValues']
        for k, v in kwargs.items():
            if k in current_state:
                current_state[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))

        return self._post(url, params, payload=current_state)
