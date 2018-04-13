class Recorder:
    """Handles recording data to a log and a database"""

    def __init__(self, database, measurement_name, logger, live):
        self.db = database
        self.measurement_name = measurement_name
        self.logger = logger
        self.live = live

    def record(self,
                schedule_state,
                current_temperature,
                minimum_temperature,
                heating_state,
                cool_down_state,

    ):
        pass

