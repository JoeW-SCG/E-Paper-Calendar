class WeatherInterface (object):
    """Interface for fetching and processing weather forecast information."""
    def is_available (self):
        raise NotImplementedError("Functions needs to be implemented")

    def get_forecast_in_days (self, offset_by_days, location):
        raise NotImplementedError("Functions needs to be implemented")

    def get_today_forecast (self, location):
        raise NotImplementedError("Functions needs to be implemented")