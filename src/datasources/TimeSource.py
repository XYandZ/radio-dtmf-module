from datetime import datetime
import logging

from src.datasources.DataSource import DataSource
from src.datasources.SourceTypes import SourceType


class TimeSource(DataSource):

    def __init__(self, code):
        self.code = code

    def assigned_code(self):
        return self.code

    @staticmethod
    def source_type():
        return SourceType.time

    def get_data(self):
        now = datetime.now()

        time_now = f"The time is{now: %-I:%M %p}"
        logging.info("Time: " + time_now)

        return time_now

    def __str__(self):
        return f"{self.code}: Current Time"