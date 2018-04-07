from pylyric.schedule import Schedule
from datetime import datetime, time


def make_schedule(start_hour):
    """Utility for building a schedule for testing."""
    return Schedule(
            active_period_start=time(start_hour, 0),
            active_period_end=time(start_hour + 1, 0),
            active_period_minimum_temperature=20.0,
            inactive_period_minimum_temperature=18.0
    )


def test_active_period():
    now = datetime.now()
    schedule = make_schedule(start_hour=now.hour)

    assert schedule.is_active_period() == True
    assert schedule.minimum_temperature == 20.0


def test_inactive_period():
    now = datetime.now()
    schedule = make_schedule(start_hour=now.hour + 1)

    assert schedule.is_active_period() == False
    assert schedule.minimum_temperature == 18.0
