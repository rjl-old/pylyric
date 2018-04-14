import datetime

from freezegun import freeze_time
from dateutil.parser import *

from pylyric.schedule import Schedule

ACTIVE_TEMPERATURE = 21.0
INACTIVE_TEMPERATURE = 19.0
ACTIVE_PERIOD_START = parse("07:00").time()
INACTIVE_PERIOD_START = parse("21:00").time()

schedule = Schedule(
        active_temperature=ACTIVE_TEMPERATURE,
        inactive_temperature=INACTIVE_TEMPERATURE,
        active_period_start=ACTIVE_PERIOD_START,
        inactive_period_start=INACTIVE_PERIOD_START,
)


class TestActivePeriodStart:
    @freeze_time("Apr 13th, 2018 01:00 ")
    def test_active_period_start_before(self):
        expected_date = parse("Apr 13th, 2018 07:00:00")
        assert schedule.active_period_start == expected_date

    @freeze_time("Apr 13th, 2018 12:00 ")
    def test_active_period_start_during(self):
        expected_date = parse("Apr 14th, 2018 07:00:00")
        assert schedule.active_period_start == expected_date

    @freeze_time("Apr 13th, 2018 23:00 ")
    def test_active_period_start_after(self):
        expected_date = parse("Apr 14th, 2018 07:00:00")
        assert schedule.active_period_start == expected_date


class TestInactivePeriodStart:
    @freeze_time("Apr 13th, 2018 01:00")
    def test_inactive_period_start_after(self):
        expected_date = parse("Apr 13th, 2018 21:00:00")
        assert schedule.inactive_period_start == expected_date

    @freeze_time("Apr 13th, 2018 12:00")
    def test_inactive_period_start_before(self):
        expected_date = parse("Apr 13th, 2018 21:00:00")
        assert schedule.inactive_period_start == expected_date

    @freeze_time("Apr 13th, 2018 23:00")
    def test_inactive_period_start_during(self):
        expected_date = parse("Apr 14th, 2018 07:00:00")
        assert schedule.inactive_period_start == expected_date
