from datetime import date
import logging

from radiodtmf.datasources.DataSource import DataSource
from radiodtmf.datasources.SourceTypes import SourceType


class DateSource(DataSource):

    def __init__(self, code):
        self.code = code

    def assigned_code(self):
        return self.code

    @staticmethod
    def source_type():
        return SourceType.date

    def get_data(self):

        today = date.today()

        todaysDate =f"Today is {today: %A, %B, %-d, %Y}"
        logging.info("Date: " + todaysDate)

        return todaysDate

    def __str__(self):
        return f"{self.code}: Current Date"