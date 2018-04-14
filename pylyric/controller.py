import datetime


class Controller:
    """Heating system controller object."""

    def __init__(self, house, schedule, warm_up_enabled=True, cool_down_enabled=True):
        self.house = house
        self.schedule = schedule
        self.warm_up_enabled = warm_up_enabled
        self.cool_down_enabled = cool_down_enabled

    def set_heating(self):
        if self.house.heating_system.is_active:
            if self.status == 'ON':
                self.house.heating_system.turn_on()
            else:
                self.house.heating_system.turn_off()

    @property
    def mode(self) -> str:
        if datetime.datetime.now() <= self.schedule.warm_up_start:
            return "INACTIVE"

        elif (not self.warm_up_enabled) and self.schedule.warm_up_start < datetime.datetime.now() <= self.schedule.active_period_start:
            return "INACTIVE"

        elif self.warm_up_enabled and self.schedule.warm_up_start < datetime.datetime.now() <= self.schedule.active_period_start:
            return "WARMUP"

        elif self.schedule.active_period_start < datetime.datetime.now() <= self.schedule.cool_down_start:
            return "ACTIVE"

        elif (not self.cool_down_enabled) and self.schedule.cool_down_start < datetime.datetime.now() <= self.schedule.inactive_period_start:
            return "ACTIVE"

        elif self.cool_down_enabled and self.schedule.cool_down_start < datetime.datetime.now() <= self.schedule.inactive_period_start:
            return "COOLDOWN"

        elif datetime.datetime.now() > self.schedule.inactive_period_start:
            return "INACTIVE"

    @property
    def hold_temperature(self):
        hold_temperatures = {
            "INACTIVE": self.schedule.inactive_temperature,
            "WARMUP": self.schedule.active_temperature if self.warm_up_enabled else self.schedule.inactive_temperature,
            "ACTIVE": self.schedule.active_temperature,
            "COOLDOWN": self.schedule.inactive_temperature if self.cool_down_enabled else self.schedule.active_temperature
        }
        return hold_temperatures[self.mode]

    @property
    def is_too_cold(self) -> bool:
        return self.house.environment_sensor.internal_temperature < self.hold_temperature

    @property
    def status(self) -> str:
        status = "ON " if self.is_too_cold else "OFF "
        status += f"({self.mode}) {self.house.environment_sensor.internal_temperature} -> {self.hold_temperature}"
        return str(status)
