

class Schedule:
    """Represents a heating schedule."""

    def __init__(self,
                     active_period_start=None,
                     active_period_end=None,
                     active_period_minimum_temperature=None,
                     inactive_period_minimum_temperature=None
                     ):

    self.active_period_start = active_period_start
    self.active_period_end = active_period_endactive_period_minimum_temperature
    self.active_period_minimum_temperature = active_period_minimum_temperature
    self.inactive_period_minimum_temperature = inactive_period_minimum_temperature