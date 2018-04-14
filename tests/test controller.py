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
schedule.active_period_start = test_date + datetime.timedelta(hours=8)
schedule.inactive_period_start = test_date + datetime.timedelta(hours=22)

# TODO: THESE ARE WRONG: CONTROLLER NOW PROVIDES .warm_up_start and .cool_down_start
schedule.warm_up_start = test_date + datetime.timedelta(hours=5)
schedule.cool_down_start = test_date + datetime.timedelta(hours=16)


class TestModeMock:

    # Early Inactive period
    @freeze_time("Apr 13th, 2018 01:00 ")
    def test_inactive_mode(self):
        assert controller.mode == "INACTIVE"

    # Warmup period, warmup disabled
    @freeze_time("Apr 13th, 2018 06:00")
    def test_warmup_mode_disabled(self):
        controller.warm_up_enabled = False
        assert controller.mode == "INACTIVE"

    # Warmup period, warmup enabled
    @freeze_time("Apr 13th, 2018 06:00")
    def test_warmup_mode_enable(self):
        controller.warm_up_enabled = True
        assert controller.mode == "WARMUP"

    # Active period
    @freeze_time("Apr 13th, 2018 12:00")  # Inactivee
    def test_warmup_mode(self):
        assert controller.mode == "ACTIVE"

    # Active period, cooldown disabled
    @freeze_time("Apr 13th, 2018 18:00")
    def test_warmup_mode(self):
        controller.cool_down_enabled = False
        assert controller.mode == "ACTIVE"

    # Active period, cooldown enabled
    @freeze_time("Apr 13th, 2018 18:00")
    def test_warmup_mode(self):
        controller.cool_down_enabled = False
        assert controller.mode == "COOLDOWN"

    # Late Inactive period
    @freeze_time("Apr 13th, 2018 23:00")
    def test_warmup_mode(self):
        assert controller.mode == "INACTIVE"


class TestIsTooColdMock:

    # controller.warm_up and controller.cool_down are True

    # GIVEN a controller
    # WHEN it's in the the INACTIVE period
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
    # WHEN it's in the the WARMUP period
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


class TestStatus:

    # Early Inactive period,
    #
    # too cold

    @freeze_time("Apr 13th, 2018 01:00 ")
    def test_inactive_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.inactive_temperature - 1
        assert controller.status == 'ON (INACTIVE) 18.0 -> 19.0'

    # Early Inactive period,
    #
    # not too cold

    @freeze_time("Apr 13th, 2018 01:00 ")
    def test_inactive_not_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.inactive_temperature + 1
        assert controller.status == 'OFF (INACTIVE) 20.0 -> 19.0'

    # Warm-up period, warm_up disabled
    #
    # too cold

    @freeze_time("Apr 13th, 2018 06:00")
    def test_warmup_disabled_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        controller.warm_up_enabled = False
        assert controller.status == 'OFF (INACTIVE) 20.0 -> 19.0'

    # Warm-up period, warm_up enabled,
    #
    # too cold

    @freeze_time("Apr 13th, 2018 06:00")
    def test_warmup_enabled_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        controller.warm_up_enabled = True
        assert controller.status == 'ON (WARMUP) 20.0 -> 21.0'

    # Active period
    #
    # too cold

    @freeze_time("Apr 13th, 2018 12:00")
    def test_active_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        assert controller.status == 'ON (ACTIVE) 20.0 -> 21.0'

    # Active period
    #
    # not too cold

    @freeze_time("Apr 13th, 2018 12:00")
    def test_active_not_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature + 1
        assert controller.status == 'OFF (ACTIVE) 22.0 -> 21.0'

    # Cool-down period, cool-down enabled,
    #
    # too cold

    @freeze_time("Apr 13th, 2018 18:00")
    def test_cooldown_enabled_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        controller.cool_down_enabled = True
        assert controller.status == 'OFF (COOLDOWN) 20.0 -> 19.0'

    # Cool-down period, cool-down enabled,
    #
    # not too cold

    @freeze_time("Apr 13th, 2018 18:00")
    def test_cooldown_disabled_not_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature + 1
        controller.cool_down_enabled = False
        assert controller.status == 'OFF (ACTIVE) 22.0 -> 21.0'

    # Late inactive period
    #
    # too cold

    @freeze_time("Apr 13th, 2018 23:00")
    def test_cooldown_enabled_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.inactive_temperature - 1
        assert controller.status == 'ON (INACTIVE) 18.0 -> 19.0'

    # Late inactive period
    #
    # not too cold

    @freeze_time("Apr 13th, 2018 23:00")
    def test_cooldown_disabled_not_too_cold(self):
        house.environment_sensor.internal_temperature = schedule.inactive_temperature + 1
        assert controller.status == 'OFF (INACTIVE) 20.0 -> 19.0'


class TestControllerWarmUpCoolDown:

    @freeze_time("Apr 13th, 2018 01:00")
    def test_warm_up_start(self):
        house.environment_sensor.internal_temperature = schedule.active_temperature - 1
        minutes = 1.0 / house.WARMUP_GRADIENT
        expected_start_time = schedule.active_period_start - datetime.timedelta(minutes=minutes)

        assert controller.warm_up_start == expected_start_time

    @freeze_time("Apr 13th, 2018 12:00")
    def test_cool_down_start(self):
        house.environment_sensor.internal_temperature = schedule.inactive_temperature + 1
        minutes = -1.0 / house.COOLDOWN_GRADIENT
        expected_start_time = schedule.inactive_period_start - datetime.timedelta(minutes=minutes)

        assert controller.cool_down_start == expected_start_time
