from datetime import date, datetime, timedelta


class Schedule:
    """Represents a heating schedule.

       A schedule is an active, an inactive period, and temperature.
    """

    def __init__(self,
                 active_temperature=None,
                 inactive_temperature=None,
                 active_period_start=None,
                 inactive_period_start=None,
                 ):

        self.active_temperature = active_temperature
        self.inactive_temperature = inactive_temperature
        self.active_period_start = active_period_start
        self.inactive_period_start = inactive_period_start

    @property
    def active_period_start(self):
        yyyy_mm_dd = date.today()
        hh_mm = self._active_period_start
        dt = datetime.combine(yyyy_mm_dd, hh_mm)

        if dt > datetime.now():
            return dt
        else:
            return dt + timedelta(days=1)

    @active_period_start.setter
    def active_period_start(self, value):
        self._active_period_start = value

    @property
    def inactive_period_start(self):
        yyyy_mm_dd = date.today()
        hh_mm_inactive = self._inactive_period_start
        hh_mm_active = self._active_period_start

        dt_inactive = datetime.combine(yyyy_mm_dd, hh_mm_inactive)
        dt_active = datetime.combine(yyyy_mm_dd, hh_mm_active)

        if dt_inactive > datetime.now():
            return dt_inactive
        else:
            return dt_active + timedelta(days=1)

    @inactive_period_start.setter
    def inactive_period_start(self, value):
        self._inactive_period_start = value
    #
    # def __repr__(self):
    #     return f"<SCHEDULE> ON:{self.active_period_start} OFF:{self.active_period_end} ACTIVE:{self.active_period_minimum_temperature} INACTIVE:{self.inactive_period_minimum_temperature}"
