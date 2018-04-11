# from datetime import datetime
from datetime import datetime, date, time, timedelta


# TODO: Need to make this time, not datetime

class Schedule:
    """Represents a heating schedule.

       A schedule is an active and an inactive period and temperature.
    """

    def __init__(self,
                 active_period_start=None,
                 active_period_end=None,
                 active_period_minimum_temperature=None,
                 inactive_period_minimum_temperature=None
                 ):

        self.active_period_start = active_period_start
        self.active_period_end = active_period_end
        self.active_period_minimum_temperature = active_period_minimum_temperature
        self.inactive_period_minimum_temperature = inactive_period_minimum_temperature

    def is_active_period(self):
        """
        :return: True if now() is in the active period
        """

        now = datetime.now()
        hh_mm = time(now.hour, now.minute)
        if self.active_period_start <= hh_mm <= self.active_period_end:
            return True
        else:
            return False

    @property
    def minimum_temperature(self):
        """
        :return: float The minimum temperature corresponding to the current period
        """
        if self.is_active_period():
            return self.active_period_minimum_temperature
        else:
            return self.inactive_period_minimum_temperature

    @property
    def period_end(self):
        """
        :return: datetime the time the current period ends
        """
        yyyy_mm_dd = date.today()

        if self.is_active_period():
            hh_mm = self.active_period_end
            dt = datetime.combine(yyyy_mm_dd, hh_mm)

        else:
            hh_mm = self.active_period_start
            dt = datetime.combine(yyyy_mm_dd, hh_mm) #+ timedelta(days=1)

        return dt
