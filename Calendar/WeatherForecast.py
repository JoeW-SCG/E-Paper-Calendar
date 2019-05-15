class WeatherForecast (object):
    """Defines a weather forecast, independent of any implementation"""
    def __init__ (self):
        self.air_temperature = None
        self.air_pressure = None
        self.air_humidity = None
        self.rain_probability = None
        self.rain_amount = None
        self.snow_amount = None
        self.sunrise = None
        self.sunset = None
        self.moon_phase = None
        self.wind_speed = None
        self.wind_deg = None
        self.clouds = None

        self.icon = None
        self.short_description = None
        self.detailed_description = None

        self.units = None
        self.datetime = None
        self.location = None
        self.fetch_datetime = None