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
                },
                "fields": kwargs
            }
        ]
        self.client.write_points(json_body)