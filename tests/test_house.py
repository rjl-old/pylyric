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

def test_is_time_to_warm_up():

    # It's cooler than the required temperature -

    REQUIRED_TEMP = 22.0
    CURRENT_TEMP = 19.0

    required_mins = int((REQUIRED_TEMP - CURRENT_TEMP) / House().WARMUP_GRADIENT)
    schedule.active_period_minimum_temperature = REQUIRED_TEMP
    environment_sensor.internal_temperature = CURRENT_TEMP

    schedule.period_end = datetime.now() + timedelta(minutes=required_mins - 10)
    assert house.is_time_to_warm_up

    schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)
    assert not house.is_time_to_warm_up

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


def test_is_time_to_cool_down():

    # It's warmer than the required temperature

    REQUIRED_TEMP = 19.0
    CURRENT_TEMP = 22.0

    required_mins = int((CURRENT_TEMP - REQUIRED_TEMP) / House().COOLDOWN_GRADIENT)
    schedule.inactive_period_minimum_temperature = REQUIRED_TEMP
    environment_sensor.internal_temperature = CURRENT_TEMP

    schedule.period_end = datetime.now() + timedelta(minutes=required_mins - 10)
    assert house.is_time_to_cool_down

    schedule.period_end = datetime.now() + timedelta(minutes=required_mins + 10)
    assert not house.is_time_to_cool_down

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

# def xtest_is_time_to_warm_up():
#     now = datetime.now()
#     schedule = Schedule(
#             active_period_start=time(now.hour, now.minute, now.second),
#             active_period_end=time(now.hour + 1, now.minute, now.second),
#             active_period_minimum_temperature=20.0,
#             inactive_period_minimum_temperature=18.0
#     )
#     print(schedule)
#     print(house.environment_sensor.internal_temperature)

# m = mock.Mock()
# m.current_temperature.return_value = 15


# @pytest.mark.parametrize(
#         "required_temperature,current_temperature,required_time, expected", [
#             (21.0, 19.0, datetime.now() + timedelta(hours=2), True),
#             (21.0, 20.5, datetime.now() + timedelta(hours=6), False)
#         ]
# )
# def test_is_time_to_warm_up(required_temperature, current_temperature, required_time, expected):
#     # required_temperature = 21.0
#     # current_temperature = 19.0
#     # required_time = datetime.now() + timedelta(hours=2)
#     assert house.is_time_to_warm_up(
#             required_temperature,
#             current_temperature,
#             required_time) == expected
