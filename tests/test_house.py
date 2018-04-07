from pylyric.house import House
from datetime import datetime, timedelta
import pytest

house = House()


@pytest.mark.parametrize(
        "required_temperature,current_temperature,required_time, expected", [
            (21.0, 19.0, datetime.now() + timedelta(hours=2), True),
            (21.0, 20.5, datetime.now() + timedelta(hours=6), False)
        ]
)
def test_is_time_to_start_heating(required_temperature, current_temperature, required_time, expected):
    # required_temperature = 21.0
    # current_temperature = 19.0
    # required_time = datetime.now() + timedelta(hours=2)
    assert house.is_time_to_start_heating(
            required_temperature,
            current_temperature,
            required_time) == expected
