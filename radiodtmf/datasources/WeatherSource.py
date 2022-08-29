import logging
import sys
import traceback
from os import environ

import pyowm

from radiodtmf.datasources.DataSource import DataSource
from radiodtmf.datasources.SourceTypes import SourceType
from radiodtmf.datasources.config import config


class WeatherSource(DataSource):

    def __init__(self, code):
        self.code = code

        # cfg = config("owm")
        #
        # self.apiKey = cfg["api_key"]
        # self.location = cfg["city"]

        self.apiKey = environ.get('OWM_API_KEY', '')
        self.location = environ.get('OWM_CITY', '')

    def assigned_code(self):
        return self.code

    @staticmethod
    def source_type():
        return SourceType.weather

    def get_data(self):
        try:
            owm = pyowm.OWM(self.apiKey)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(self.location)
            # observation = forecaster.get_forecast()
            w = observation
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            logging.exception(lines)
            logging.warning("Weather Offline")
            return "Sorry. The weather is Offline"

        windData = w.weather.wind(unit='knots')
        windSpeed = round(windData['speed'])
        windDirection = windData['deg']

        temp = w.weather.temperature('fahrenheit')['temp']
        rh = w.weather.barometric_pressure()['press']

        report = f"Current Weather: Air temperature, {temp} Farenheit. Barometric pressure {rh} HPA. Wind Speed, {windSpeed} knots at {windDirection} degrees."
        logging.info("Weather: " + report)

        return report

    def __str__(self):
        return f"{self.code}: Current Weather"
