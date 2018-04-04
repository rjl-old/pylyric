#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from pylyric.device import Device


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
    See: https://developer.honeywell.com/api-methods?field_smart_method_tags_tid=All
    """

    trace_out = False

    def __init__(self, client_credentials_manager=None):
        """
        Create a Lyric API object
        :param auth: An authorisation token (optional)
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

        r = self._session.request(method, url, headers=headers, **args)

        if self.trace_out:
            print('>> headers', headers)
            print('>> http status', r.status_code)
            print('>>', method, r.url)
            if payload:
                print(">> DATA", json.dumps(payload))
        try:
            r.raise_for_status()
        except:
            raise LyricException(r.status_code, -1, '%s:\n %s' % (r.url, r.json()), headers=r.headers)
        finally:
            r.connection.close()

        if r.text and len(r.text) > 0 and r.text != 'null':
            results = r.json()
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

    def devices(self, locationID):
        """
        https://developer.honeywell.com/lyric/apis/get/devices
        :param locationID: int
        :return: list of dict of device properties
        """
        params = {"locationId": locationID}
        json = self._get('devices', params)
        return json

    def device(self, locationID, deviceID):
        """
        https://developer.honeywell.com/lyric/apis/get/devices/thermostats/%7BdeviceId%7D-0
        :param locationID:
        :return: dict of device properties
        """
        url = "devices/thermostats/{}".format(deviceID)
        params = {"locationId": locationID}
        json = self._get(url, params)
        return json

    def change_device(self, locationID, deviceID, **kwargs):
        """
        https://developer.honeywell.com/lyric/apis/post/devices/thermostats/%7BdeviceId%7D
        :param locationID: int
        :param deviceID: int
        :return:
        """
        url = "devices/thermostats/{}".format(deviceID)
        params = {"locationId": locationID}

        current_state = self.device(locationID, deviceID)['changeableValues']
        for k, v in kwargs.items():
            if k in current_state:
                current_state[k] = v
            else:
                raise Exception("Unknown parameter: '{}'".format(k))

        return self._post(url, params, payload=current_state)
