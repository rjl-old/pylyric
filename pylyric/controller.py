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
        if datetime.datetime.now() <= self.warm_up_start:
            return "INACTIVE"

        elif (
                not self.warm_up_enabled) and self.warm_up_start < datetime.datetime.now() <= self.schedule.active_period_start:
            return "INACTIVE"

        elif self.warm_up_enabled and self.warm_up_start < datetime.datetime.now() <= self.schedule.active_period_start:
            return "WARMUP"

        elif self.schedule.active_period_start < datetime.datetime.now() <= self.cool_down_start:
            return "ACTIVE"

        elif (
                not self.cool_down_enabled) and self.cool_down_start < datetime.datetime.now() <= self.schedule.inactive_period_start:
            return "ACTIVE"

        elif self.cool_down_enabled and self.cool_down_start < datetime.datetime.now() <= self.schedule.inactive_period_start:
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
    def warm_up_start(self) -> datetime:
        """Return the time to start heating the house to achieve the active period temperature."""
        temperature_change = self.schedule.active_temperature - self.house.environment_sensor.internal_temperature
        required_minutes = temperature_change / self.house.WARMUP_GRADIENT

        return self.schedule.active_period_start - datetime.timedelta(minutes=required_minutes)

    @property
    def cool_down_start(self) -> datetime:
        """Return the time to start cooling the house to achieve the inactive period temperature."""
        temperature_change = self.schedule.inactive_temperature - self.house.environment_sensor.internal_temperature
        required_minutes = temperature_change / self.house.COOLDOWN_GRADIENT

        return self.schedule.inactive_period_start - datetime.timedelta(minutes=required_minutes)

    @property
    def is_boiler_on(self) -> bool:
        return True if self.house.heating_system.is_active and self.is_too_cold else False

    @property
    def status(self) -> str:
        internal_temperature = round(self.house.environment_sensor.internal_temperature, 1)
        hold_temperature = round(self.hold_temperature, 1)
        status = "ON " if self.is_boiler_on else "OFF "
        status += f"({self.mode}) {internal_temperature} -> {hold_temperature}"
        return str(status)
