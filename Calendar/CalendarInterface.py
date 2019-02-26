from DataSourceInterface import DataSourceInterface

class CalendarInterface (DataSourceInterface):
    """Interface for fetching and processing calendar event information."""
    def get_upcoming_events(self):
        raise NotImplementedError("Functions needs to be implemented")

    def get_today_events(self):
        raise NotImplementedError("Functions needs to be implemented")

    def get_day_events(self, date):
        raise NotImplementedError("Functions needs to be implemented")

    def get_month_events(self, month = -1):
        raise NotImplementedError("Functions needs to be implemented")

    def get_week_events(self, week = -1):
        raise NotImplementedError("Functions needs to be implemented")