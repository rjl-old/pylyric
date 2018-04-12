from datetime import date, datetime, time


class Schedule:
    """Represents a heating schedule.

       A schedule is an active, an inactive period, and temperature.
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
        return True if self.active_period_start <= hh_mm <= self.active_period_end else False

    @property
    def minimum_temperature(self):
        """
        :return: float The minimum temperature corresponding to the current period
        """
        return self.active_period_minimum_temperature if self.is_active_period() else self.inactive_period_minimum_temperature

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
            dt = datetime.combine(yyyy_mm_dd, hh_mm)  # + timedelta(days=1)

        return dt

    def __repr__(self):
        return f"<SCHEDULE> ON:{self.active_period_start} OFF:{self.active_period_end} ACTIVE:{self.active_period_minimum_temperature} INACTIVE:{self.inactive_period_minimum_temperature}"
