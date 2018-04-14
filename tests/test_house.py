from datetime import datetime, timedelta
from unittest import mock

from pylyric.house import House

environment_sensor = mock.Mock()
heating_system = mock.Mock()
schedule = mock.Mock()

house = House(
        environment_sensor=environment_sensor,
        heating_system=heating_system,
        schedule=schedule)


# NOTE: These tests depend on the class's thermal gradient settings

class TestIsTimeToWarmUp:

    def test_is_cooler_than_required(self):

        # It's cooler than the required temperature -

        REQUIRED_TEMP = 22.0
        CURRENT_TEMP = 19.0

        required_mins = int((REQUIRED_TEMP - CURRENT_TEMP) / House().WARMUP_GRADIENT)
        schedule.active_period_minimum_temperature = REQUIRED_TEMP
        environment_sensor.internal_temperature = CURRENT_TEMP

        # and it's time to warm up
        schedule.period_end = datetime.now() + timedelta(minutes=required_mins - 10)
        assert house.is_time_to_warm_up

        # and it's not time to warm up
        schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)
        assert not house.is_time_to_warm_up

    def test_is_warmer_than_required(self):

        # It's warmer than the required temperature - should always fail

        REQUIRED_TEMP = 19.0
        CURRENT_TEMP = 22.0

        required_mins = int((REQUIRED_TEMP - CURRENT_TEMP) / House().WARMUP_GRADIENT)
        schedule.active_period_minimum_temperature = REQUIRED_TEMP
        environment_sensor.internal_temperature = CURRENT_TEMP

        schedule.period_end = datetime.now() + timedelta(minutes=required_mins - 10)
        assert not house.is_time_to_warm_up

        schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)
        assert not house.is_time_to_warm_up

class TestIsTimeToCoolDown:

    def test_is_warmer_than_required(self):

        # It's warmer than the required temperature

        REQUIRED_TEMP = 19.0
        CURRENT_TEMP = 22.0

        required_mins = int((CURRENT_TEMP - REQUIRED_TEMP) / House().COOLDOWN_GRADIENT)
        schedule.inactive_period_minimum_temperature = REQUIRED_TEMP
        environment_sensor.internal_temperature = CURRENT_TEMP

        # it's time to cool down
        schedule.period_end = datetime.now() + timedelta(minutes=required_mins - 10)
        assert house.is_time_to_cool_down

        # it's not time to cool down
        schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)
        assert not house.is_time_to_cool_down

    def test_is_cooler_than_required(self):

        # It's cooler than the required temperature - should always fail

        REQUIRED_TEMP = 22.0
        CURRENT_TEMP = 19.0

        required_mins = int((CURRENT_TEMP - REQUIRED_TEMP) / House().COOLDOWN_GRADIENT)
        schedule.inactive_period_minimum_temperature = REQUIRED_TEMP
        environment_sensor.internal_temperature = CURRENT_TEMP

        schedule.period_end = datetime.now() + timedelta(minutes=required_mins - 10)
        assert not house.is_time_to_cool_down

        schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)
        assert not house.is_time_to_cool_down

class TestMode:

    # ON - active or inactive period, heating is on and it's not time to cool down
    # OFF - active or inactive period, heating is off and it's not time to warm up
    # WARM-UP - inactive period and it's time to warm up
    # COOL-DOWN - active period and it's time to cool down

    def test_mode_OFF(self):

        # heating is off
        heating_system.is_on = False

        # it's not time to warm up
        REQUIRED_TEMP = 22.0
        CURRENT_TEMP = 19.0

        required_mins = int((REQUIRED_TEMP - CURRENT_TEMP) / House().WARMUP_GRADIENT)
        schedule.active_period_minimum_temperature = REQUIRED_TEMP
        environment_sensor.internal_temperature = CURRENT_TEMP
        schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)

        assert house.mode == "OFF"

    def test_mode_ON(self):

        # heating is on
        heating_system.is_on = True

        # it's not time to cool down
        REQUIRED_TEMP = 19.0
        CURRENT_TEMP = 22.0

        required_mins = int((CURRENT_TEMP - REQUIRED_TEMP) / House().COOLDOWN_GRADIENT)
        schedule.inactive_period_minimum_temperature = REQUIRED_TEMP
        environment_sensor.internal_temperature = CURRENT_TEMP

        schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)

        assert house.mode == "ON"

    def test_mode_WARMUP(self):

        # it's the inactive period
        schedule.is_active_period = False

        # and it's time to warm up
        REQUIRED_TEMP = 22.0
        CURRENT_TEMP = 19.0

        required_mins = int((REQUIRED_TEMP - CURRENT_TEMP) / House().WARMUP_GRADIENT)
        schedule.active_period_minimum_temperature = REQUIRED_TEMP
        environment_sensor.internal_temperature = CURRENT_TEMP
        schedule.period_end = datetime.now() + timedelta(minutes=required_mins - 10)

        assert house.mode == "WARM-UP"

