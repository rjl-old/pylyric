from pylyric.schedule import Schedule
from datetime import datetime, timedelta


def make_schedule(start_time):
    return Schedule(
            active_period_start=start_time,
            active_period_end=start_time + timedelta(hours=1),
            active_period_minimum_temperature=20.0,
            inactive_period_minimum_temperature=18.0
    )


def test_initialise():
    t = datetime.now()
    print(make_schedule(start_time=t))


def test_active_period():
    # GIVEN a valid schedule
    # WHEN the current time is an active period
    # THEN return True and the active temperature
    schedule = make_schedule(start_time=datetime.now())
    assert schedule.is_active_period() == True
    assert schedule.minimum_temperature == 20.0


def test_inactive_period():
    # GIVEN a valid schedule
    # WHEN the current time is an inactive period
    # THEN return False and the inactive temperature
    schedule = make_schedule(start_time=(datetime.now() + timedelta(hours=1)))
    assert schedule.is_active_period() == False
    assert schedule.minimum_temperature == 18.0
