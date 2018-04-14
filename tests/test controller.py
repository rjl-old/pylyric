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

class TestIsTooCold:

    # controller.warm_up and controller.cool_down are True

    # GIVEN a controller
    # WHEN it's in the the INACTIVE mode
    # AND the internal temperature is less than the inactive hold temperature
    # THEN it is too cold

    @freeze_time("Apr 13th, 2018 01:00 ")
    def test_inactive_is_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.inactive_temperature - 1
        assert controller.is_too_cold == True

    @freeze_time("Apr 13th, 2018 01:00 ")
    def test_inactive_is_not_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.inactive_temperature + 1
        assert controller.is_too_cold == False

    # GIVEN a controller
    # WHEN it's in the the WARMUP mode
    # AND .warm_up is True
    # AND the internal temperature is less than the active hold temperature
    # THEN it is too cold

    @freeze_time("Apr 13th, 2018 06:00 ")
    def test_warmup_is_not_too_cold(self):
        controller.warm_up = True
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        assert controller.is_too_cold == True

    @freeze_time("Apr 13th, 2018 06:00 ")
    def test_warmup_is_not_too_cold(self):
        controller.warm_up = True
        house.environment_sensor.internal_temperature = schedule.active_temperature + 1
        assert controller.is_too_cold == False

    # GIVEN a controller
    # WHEN it's in the the WARMUP mode
    # AND .warm_up is False
    # AND the internal temperature is less than the inactive hold temperature
    # THEN it is too cold

    @freeze_time("Apr 13th, 2018 06:00 ")
    def test_warmup_is_not_too_cold_if_no_warmup(self):
        controller.warm_up = False
        house.environment_sensor.internal_temperature = schedule.inactive_temperature - 1
        assert controller.is_too_cold == True

    @freeze_time("Apr 13th, 2018 06:00 ")
    def test_warmup_is_not_too_cold_if_no_warmup(self):
        controller.warm_up = False
        house.environment_sensor.internal_temperature = schedule.inactive_temperature + 1
        assert controller.is_too_cold == False

    # GIVEN a controller
    # WHEN it's in the the ACTIVE mode
    # AND the internal temperature is less than the active hold temperature
    # THEN it is too cold

    @freeze_time("Apr 13th, 2018 12:00 ")
    def test_active_is_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        assert controller.is_too_cold == True

    @freeze_time("Apr 13th, 2018 12:00 ")
    def test_active_is_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature + 1
        assert controller.is_too_cold == False

    # GIVEN a controller
    # WHEN it's in the the COOLDOWN mode
    # AND .cool_down is True
    # AND the internal temperature is less than the inactive hold temperature
    # THEN it is too cold

    @freeze_time("Apr 13th, 2018 18:00 ")
    def test_cooldown_is_too_cold(self):
        controller.cool_down = True
        house.environment_sensor.internal_temperature = schedule.inactive_temperature - 1
        assert controller.is_too_cold == True

    @freeze_time("Apr 13th, 2018 18:00 ")
    def test_cooldown_is_not_too_cold(self):
        controller.cool_down = True
        house.environment_sensor.internal_temperature = schedule.inactive_temperature + 1
        assert controller.is_too_cold == False

    # GIVEN a controller
    # WHEN it's in the COOLDOWN period
    # AND .cool_down is False
    # and the internal temperature is less than the active hold temperature
    # THEN it is too cold

    @freeze_time("Apr 13th, 2018 18:00 ")
    def test_warmup_is_not_too_cold_if_no_warmup(self):
        controller.cool_down = False
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        assert controller.is_too_cold == True

    @freeze_time("Apr 13th, 2018 18:00 ")
    def test_warmup_is_not_too_cold_if_no_warmup(self):
        controller.cool_down = False
        house.environment_sensor.internal_temperature = schedule.active_temperature + 1
        assert controller.is_too_cold == False



