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


def record(db, controller):
    """Records the status of the controller to the database"""

    db.write("controller",
             hold_temperature=controller.hold_temperature,
             heating=controller.is_boiler_on,
             active=controller.mode == 'ACTIVE',
             inactive=controller.mode == 'INACTIVE',
             warmup=controller.mode == 'WARMUP',
             cooldown=controller.mode == 'COOLDOWN',
             )
