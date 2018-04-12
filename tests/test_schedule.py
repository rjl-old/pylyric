from pylyric.schedule import Schedule
from datetime import datetime, time, date


def make_schedule(start_hour):
    """Utility for building a schedule for testing. Makes sure that now() is an active or inactive period
    """
    return Schedule(
            active_period_start=time(start_hour, 0),
            active_period_end=time(start_hour + 1, 0),
            active_period_minimum_temperature=20.0,
            inactive_period_minimum_temperature=18.0
    )


def test_is_active_period():
    now = datetime.now()
    schedule = make_schedule(start_hour=now.hour)
    assert schedule.is_active_period() == True
    assert schedule.minimum_temperature == 20.0


def test_active_period_end():
    now = datetime.now()
    yyyy_mm_dd = date.today()
    hh_mm = time(now.hour + 1)
    expected_end = datetime.combine(yyyy_mm_dd, hh_mm)

    schedule = make_schedule(start_hour=now.hour)
    assert schedule.period_end == expected_end


def test_inactive_period_end():
    now = datetime.now()
    yyyy_mm_dd = date.today()
    hh_mm = time(now.hour + 1)
    expected_end = datetime.combine(yyyy_mm_dd, hh_mm)

    schedule = make_schedule(start_hour=now.hour + 1)
    assert schedule.period_end == expected_end


def test_is_not_active_period():
    now = datetime.now()
    schedule = make_schedule(start_hour=now.hour + 1)

    assert schedule.is_active_period() == False
    assert schedule.minimum_temperature == 18.0
