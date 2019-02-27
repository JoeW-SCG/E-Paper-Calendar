from WeatherForecast import WeatherForecast
from WeatherInterface import WeatherInterface
import pyowm
from datetime import datetime
from settings import units

class OwmForecasts (WeatherInterface):
    """Fetches weather through the Openweathermap-api."""
    def __init__ (self, api_key):
        self.api = pyowm.OWM(api_key)
        self.units = units

    def is_available (self):
        try:
            return self.api.is_API_online()
        except:
            return False

    def get_today_forecast (self, location):
        if self.is_available() is False:
            return None

        observation = self.api.weather_at_place(location)
        weather = observation.get_weather()

        return self.__get_forecast_from_weather__(weather, location=location)

    def get_forecast_in_days (self, offset_by_days, location):
        return None

    def __get_forecast_from_weather__ (self, weather, location):
        forecast_object = WeatherForecast()
        forecast_object.units = self.units
        forecast_object.fetch_time = datetime.now()
        forecast_object.location = location
        forecast_object.forecast_datetime = weather.get_reference_time(timeformat='date')

        forecast_object.icon = weather.get_weather_icon_name()
        forecast_object.air_humidity = str(weather.get_humidity())
        forecast_object.clouds = str(weather.get_clouds())
        forecast_object.short_description = str(weather.get_status())
        forecast_object.detailed_description = str(weather.get_detailed_status())
        forecast_object.air_pressure = str(weather.get_pressure()['press'])

        if forecast_object.units == "metric":
            forecast_object.air_temperature = str(int(weather.get_temperature(unit='celsius')['temp']))
            forecast_object.wind_speed = str(int(weather.get_wind()['speed']))

        if forecast_object.units == "imperial":
            forecast_object.air_temperature = str(int(weather.get_temperature('fahrenheit')['temp']))
            forecast_object.wind_speed = str(int(weather.get_wind()['speed'] * 0.621))

        forecast_object.sunrise = datetime.fromtimestamp(int(weather.get_sunrise_time(timeformat='unix')))
        forecast_object.sunset = datetime.fromtimestamp(int(weather.get_sunset_time(timeformat='unix')))

        return forecast_object