import server.config as cfg
from influxdb import InfluxDBClient


class Influx:

    def __init__(self, db_name):
        host = cfg.IP
        port = cfg.PORT
        user = cfg.USERNAME
        password = cfg.PASSWORD
        db_name = db_name

        self.client = InfluxDBClient(host, port, user, password, db_name)

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
