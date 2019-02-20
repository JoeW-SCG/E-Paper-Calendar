class WeatherForecast (object):
    """Defines a weather forecast, independent of any implementation"""
    def __init__ (self):
        self.air_temperature = None
        self.rain_probability = None
        self.rain_amount = None
        self.sunrise = None
        self.sunset = None
        self.moon_phase = None
        self.wind_speed = None

        self.icon = None
        self.short_description = None

        self.date = None
        self.place = None
        self.fetch_time = None