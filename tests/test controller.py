import datetime
from unittest import mock

from dateutil.parser import *
from freezegun import freeze_time

from pylyric.controller import Controller

environment_sensor = mock.Mock(name="EnvironmentSensor")
heating_system = mock.Mock(name="HeatingSystem")

house = mock.Mock(name="House")
house.environment_sensor = environment_sensor
house.heating_system = heating_system
house.WARMUP_GRADIENT = 0.001637426900584798
house.COOLDOWN_GRADIENT = -0.001825459656038644

schedule = mock.Mock(name="Schedule")
schedule.active_temperature = 21.0
schedule.inactive_temperature = 19.0

controller = Controller(house=house, schedule=schedule)

test_date = parse("Apr 13th, 2018 00:00:00")
schedule.warm_up_start = test_date + datetime.timedelta(hours=5)
schedule.active_period_start = test_date + datetime.timedelta(hours=8)
schedule.cool_down_start = test_date + datetime.timedelta(hours=16)
schedule.inactive_period_start = test_date + datetime.timedelta(hours=22)


class TestMode:

    @freeze_time("Apr 13th, 2018 01:00 ")
    def test_inactive_mode(self):
        assert controller.mode == "INACTIVE"

    @freeze_time("Apr 13th, 2018 06:00")
    def test_warmup_mode(self):
        assert controller.mode == "WARMUP"

    @freeze_time("Apr 13th, 2018 12:00")
    def test_warmup_mode(self):
        assert controller.mode == "ACTIVE"

    @freeze_time("Apr 13th, 2018 18:00")
    def test_warmup_mode(self):
        assert controller.mode == "COOLDOWN"

    @freeze_time("Apr 13th, 2018 23:00")
    def test_warmup_mode(self):
        assert controller.mode == "INACTIVE"
