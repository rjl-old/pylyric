import datetime


class Controller:
    """Heating system controller object."""

    def __init__(self, house, schedule):
        self.house = house
        self.schedule = schedule

    @property
    def mode(self):
        if datetime.datetime.now() <= self.schedule.warm_up_start:
            return "INACTIVE"
        elif self.schedule.warm_up_start < datetime.datetime.now() <= self.schedule.active_period_start:
            return "WARMUP"
        elif self.schedule.active_period_start < datetime.datetime.now() <= self.schedule.cool_down_start:
            return "ACTIVE"
        elif self.schedule.cool_down_start < datetime.datetime.now() <= self.schedule.inactive_period_start:
            return "COOLDOWN"
        elif datetime.datetime.now() > self.schedule.inactive_period_start:
            return "INACTIVE"
