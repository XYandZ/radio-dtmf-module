import logging
import sys
import traceback
from os import environ
import smbus2
import bme280

from radiodtmf.datasources.DataSource import DataSource
from radiodtmf.datasources.SourceTypes import SourceType


class BME280Source(DataSource):

    def __init__(self, code):
        self.code = code

        self.__ic2_port = int(environ.get('BME280_IC2_PORT', '1'))
        self.__ic2_bus = smbus2.SMBus(self.__ic2_port)
        self.__ic2_address = int(environ.get('BME280_IC2_ADDRESS', '0x76'), 0)

        self.__bme280_calibration_params = bme280.load_calibration_params(self.__ic2_bus, self.__ic2_address)

    def assigned_code(self):
        return self.code

    @staticmethod
    def source_type():
        return SourceType.bme280

    def get_data(self):
        bme280_sample = bme280.sample(self.__ic2_bus, self.__ic2_address, self.__bme280_calibration_params)

        temp_c = bme280_sample.temperature
        temp_f = (temp_c * 9/5) + 32
        rh = bme280_sample.pressure
        humidity = bme280_sample.humidity

        # Round all floats to one decimal place so the TTS doesn't take forever to read things out
        temp_f_str = "{:.1f}".format(temp_f)
        rh_str = "{:.1f}".format(rh)
        humidity_str = "{:.1f}".format(humidity)

        report = f"Current Weather: Air temperature, {temp_f_str} Farenheit. Barometric pressure {rh_str} HPA. " \
                 f"Humidity, {humidity_str} % rH. "
        logging.info("Weather: " + report)

        return report

    def __str__(self):
        return f"{self.code}: Current Weather"
