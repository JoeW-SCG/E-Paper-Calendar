from DataSourceInterface import DataSourceInterface
from datetime import datetime, timezone, timedelta

class CalendarInterface (DataSourceInterface):
    """Interface for fetching and processing calendar event information."""
    def __init__(self):
        self.loaded_events = self.__get_events__()
        self.__sort_events__()

    def __sort_events__(self):
        self.loaded_events.sort(key=lambda x : x.begin_datetime)

    def __get_events__(self):
        raise NotImplementedError("Functions needs to be implemented")

    def get_upcoming_events(self):
        return self.__get_events_to_filter__(lambda x : (x.begin_datetime - datetime.now(timezone.utc)) > timedelta(days=-1))

    def get_today_events(self):
        return self.get_day_events(datetime.now(timezone.utc))

    def get_day_events(self, date):
        if type(date) is type(datetime.now()):
            date = date.date()
        return self.__get_events_to_filter__(lambda x : (x.begin_datetime.date() - date) <= timedelta(0) and (x.end_datetime.date() - date) >= timedelta(0))

    def get_month_events(self, month = -1):
        if month < 0:
            month = datetime.now().month
        return self.__get_events_to_filter__(lambda x : x.begin_datetime.month == month)

    def get_week_events(self, week = -1):
        if week < 0 and week_starts_on == "Monday":
            week = int(datetime.now().strftime('%W')) + 1
        elif week < 0:
            week = int(datetime.now().strftime('%U')) + 1

        if week_starts_on == "Monday":
            return self.__get_events_to_filter__(lambda x : int(x.begin_datetime.strftime('%W')) + 1 == week)
        else:
            return self.__get_events_to_filter__(lambda x : int(x.begin_datetime.strftime('%U')) + 1 == week)

    def __get_events_to_filter__(self, event_filter):
        if self.loaded_events is None:
            return []
        return [event for event in self.loaded_events if event_filter(event)]