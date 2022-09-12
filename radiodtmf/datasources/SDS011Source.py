import logging
from os import environ
import aqi
from sds011 import SDS011

from radiodtmf.datasources.DataSource import DataSource
from radiodtmf.datasources.SourceTypes import SourceType


class SDS011Source(DataSource):

    def __init__(self, code):
        self.code = code

        sds011_dev = environ.get('SDS011_DEV', '/dev/ttyUSB0')
        self.__sds = SDS011(port=sds011_dev)
        self.__sds.set_working_period(rate=1)

    def assigned_code(self):
        return self.code

    @staticmethod
    def source_type():
        return SourceType.sds011

    def get_data(self):
        sample = self.__sds.read_measurement()

        pm2_5_measurement = sample['pm2.5']
        pm10_measurement = sample['pm10']
        # Native units are ug/m3; we need to convert to AQI.

        # Round all floats to one decimal place, so they can be fed into aqi estimation
        pm2_5_str = "{:.1f}".format(pm2_5_measurement)
        pm10_str = "{:.1f}".format(pm10_measurement)

        # Estimate current AQI using instantaneous PM2.5 and PM10 values.
        # Note true AQI needs to be average over a 24-hour period.
        estimated_aqi = aqi.to_aqi([
            (aqi.POLLUTANT_PM25, pm2_5_str),
            (aqi.POLLUTANT_PM10, pm10_str)
        ])

        report = f"Air Quality Index: {estimated_aqi}"
        logging.info("Air Quality: " + report)

        return report

    def __str__(self):
        return f"{self.code}: Current Air Quality"
