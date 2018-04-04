import pylyric.config as cfg
from influxdb import InfluxDBClient
import datetime


class Influx:

    def __init__(self):
        host = cfg.IP
        port = cfg.PORT
        user = cfg.USERNAME
        password = cfg.PASSWORD
        dbname = "test"

        self.client = InfluxDBClient(host, port, user, password, dbname)

    def write(self, measurement, **kwargs):
        json_body = [
            {
                "measurement": "{}".format(measurement),
                "tags": {
                    "host": "server01",
                    "region": "us-west"
                },
                "fields": {
                    "Float_value": 0.64,
                    "Int_value": 3,
                    "String_value": "Text",
                    "Bool_value": True
                }
            }
        ]
        self.client.write_points(json_body)