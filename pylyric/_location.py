import json
from typing import Dict, List

from pylyric.device import Device


class Location:
    """
    Represents a location from the Lyric API
    """

    def __init__(
            self,
            lyric_api,
            location_id: int,
            name: str,
            street_address: str,
            city: str,
            country: str,
            zip_code: str,
            devices: List[Device] or List[dict] or str,
            users: List[Dict] or str
    ):
        """

        :param client:
        :param location_id:
        :param name:
        :param street_address:
        :param city:
        :param country:
        :param zip_code:
        :param devices: A list of devices or string representation.
        :param users: A list of users or string representation.
        """
        self.lyric_api = lyric_api
        self.location_id = location_id
        self.name = name
        self.street_address = street_address
        self.city = city
        self.country = country
        self.zip_code = zip_code
        self._devices = devices
        self._users = users

    def get_devices(self) -> List[Device]:
        """
        Lazy loads a list of devices at a given location.
        :return:
        """
        if isinstance(self._devices, str):
            self._devices = json.loads(self._devices)
        if len(self._devices) > 0 and isinstance(self._devices[0], dict):
            self._devices = [Device.from_json(self.location_id, self.lyric_api, data) for data in self._devices]

        return self._devices

    def get_users(self) -> List[Dict]:
        """
        Lazy loads the list of users.
        :return:
        """
        if isinstance(self._users, str):
            self._users = json.loads(self._users)

        return self._users

    @classmethod
    def from_json(cls, lyric_api, data: str or Dict) -> 'Location':
        """
        Converts a json object or string representation
        into a honeywell location.
        :param lyric_api: The client to use to update.
        :param data: The data in string or dict form.
        :return: A location object for that data.
        """
        if isinstance(data, str):
            data = json.loads(data)

        return cls(
            lyric_api,
            data["locationID"],
            data["name"],
            data["streetAddress"],
            data["city"],
            data["country"],
            data["zipcode"],
            data["devices"],
            data["users"],
        )