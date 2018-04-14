import datetime


class Controller:
    """Heating system controller object."""

    def __init__(self, house, schedule, warm_up=True, cool_down=True):
        self.house = house
        self.schedule = schedule
        self.warm_up = warm_up
        self.cool_down = cool_down

    @property
    def mode(self) -> str:
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

    @property
    def is_too_cold(self) -> bool:
        hold_temperatures = {
            "INACTIVE": self.schedule.inactive_temperature,
            "WARMUP": self.schedule.active_temperature if self.warm_up else self.schedule.inactive_temperature,
            "ACTIVE": self.schedule.active_temperature,
            "COOLDOWN": self.schedule.inactive_temperature if self.cool_down else self.schedule.active_temperature
        }
        hold_temperature = hold_temperatures[self.mode]
        return self.house.environment_sensor.internal_temperature < hold_temperature