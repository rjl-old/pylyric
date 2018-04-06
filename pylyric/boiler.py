import requests


class Boiler:
    """This class represents a boler"""

    HONEYWELL_API = "https://api.honeywell.com/v2/"
    LOCATION_ID = None
    DEVICE_ID = None

    def turn_on(self):
        url = self.HONEYWELL_API + "https://api.honeywell.com/v2/"
