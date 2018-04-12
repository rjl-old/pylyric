from datetime import datetime, time
from unittest import mock

from pylyric.environment_sensor import EnvironmentSensor
from pylyric.house import House
from pylyric.photon import Photon
from pylyric.schedule import Schedule

# PHOTON_DEVICE_ID = "37002b001147343438323536"
# photon = Photon(device_id=PHOTON_DEVICE_ID)
mock_photon = mock.Mock()
mock_photon.internal_temperature.return_value = 15
environment_sensor: EnvironmentSensor = mock_photon
house = House(environment_sensor=environment_sensor)

def test_mock_object():
    mock_photon = mock.Mock()
    environment_sensor: EnvironmentSensor = mock_photon
    house = House(environment_sensor=environment_sensor)
    mock_photon.internal_temperature.assert_called_with()


def xtest_is_time_to_warm_up():
    now = datetime.now()
    schedule = Schedule(
            active_period_start=time(now.hour, now.minute, now.second),
            active_period_end=time(now.hour + 1, now.minute, now.second),
            active_period_minimum_temperature=20.0,
            inactive_period_minimum_temperature=18.0
    )
    print(schedule)
    print(house.environment_sensor.internal_temperature)

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
