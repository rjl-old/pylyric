import base64
import json
import os



def print_authorisation():
    """prints the base64 encoded result of id:secret
       -> G84Tia8JeST2ELVBqWQWRdZ4cQuqWKZM
    """
    config_file = os.path.join((os.path.abspath(os.path.dirname(__file__))), "auth.json")
    with open(config_file) as json_file:
        config_data = json.load(json_file)

    string = "{}:{}".format(config_data['client']['client_id'], config_data['client']['client_secret'])
    print(base64.b64encode(string.encode('utf-8')))


def protector(func):
    """Decorator for LyricAPI methods"""
    def retried_func(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            if resp.status_code != 200:
                raise ApiError(
                        resp.status_code,
                        resp.reason,
                        resp.url)
            return resp

        except Exception as x:
            print(f'{x.__class__.__name__}::honeywellAPI.{func.__name__}() [{x}]')

    return retried_func
