from DebugInterface import DebugInterface
from icon_positions_locations import weathericons

class DebugConsole (DebugInterface):
    """Defines concrete console export of debug objects"""
    def print_event (self, event):
        print("\nCalendarEvent:")
        print("---------------------")
        print('Begin datetime: ' + str(event.begin_datetime))
        print('End datetime: ' + str(event.end_datetime))
        print('Title: ' + str(event.title))
        print('Description: ' + str(event.description))
        print('Attendees: ' + str(event.attendees))
        print('Highlight: ' + str(event.highlight))
        print('Calendar name: ' + str(event.calendar_name))
        print('Location: ' + str(event.location))
        print('Fetch datetime: ' + str(event.fetch_datetime))

    def print_forecast (self, forecast):
        print("\nWeatherForecast:")
        print("---------------------")
        print('Air temperature: ' + str(forecast.air_temperature))
        print('Air humidity: ' + str(forecast.air_humidity))
        print('Air pressure: ' + str(forecast.air_pressure))
        print('Rain probability: ' + str(forecast.rain_probability))
        print('Rain amount: ' + str(forecast.rain_amount))
        print('Snow amount: ' + str(forecast.snow_amount))
        print('Sunrise-time: ' + str(forecast.sunrise))
        print('Sunset time: ' + str(forecast.sunset))
        print('Moon phase: ' + str(forecast.moon_phase))
        print('Wind speed: ' + str(forecast.wind_speed))
        print('Cloudiness: ' + str(forecast.clouds))
        print('Icon code: ' + str(forecast.icon))
        print('weather-icon name: ' + str(weathericons[forecast.icon]))
        print('Short description: ' + str(forecast.short_description))
        print('Detailed description: ' + str(forecast.detailed_description))
        print('Units: ' + str(forecast.units))
        print('Datetime: ' + str(forecast.datetime))
        print('Location: ' + str(forecast.location))
        print('Fetch datetime: ' + str(forecast.fetch_datetime))

    def print (self, content):
        if content is None:
            return
        print(str(content))