import logging
import sys
import traceback
from os import environ
import smbus2
import bme280

from src.datasources.DataSource import DataSource
from src.datasources.SourceTypes import SourceType


class WeatherSource(DataSource):

    def __init__(self, code):
        self.code = code

        self.__ic2_port = int(environ.get('BME280_IC2_PORT', '1'))
        self.__ic2_bus = smbus2.SMBus(self.__ic2_port)
        self.__ic2_address = environ.get('BME280_IC2_ADDRESS', '0x76')

        self.__bme280_calibration_params = bme280.load_calibration_params(self.__ic2_bus, self.__ic2_address)

    def assigned_code(self):
        return self.code

    @staticmethod
    def source_type():
        return SourceType.weather

    def get_data(self):
        bme280_sample = bme280.sample(self.__ic2_bus, self.__ic2_address, self.__bme280_calibration_params)

        temp_c = bme280_sample.temperature
        temp_f = (temp_c * 9/5) + 32
        rh = bme280_sample.pressure
        humidity = bme280_sample.humidity

        report = f"Current Weather: Air temperature, {temp_f} Farenheit. Barometric pressure {rh} HPA. Humidity, {humidity} % rH."
        logging.info("Weather: " + report)

        return report

    def __str__(self):
        return f"{self.code}: Current Weather"
