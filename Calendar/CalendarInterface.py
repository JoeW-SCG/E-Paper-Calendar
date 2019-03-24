from DataSourceInterface import DataSourceInterface
from datetime import datetime, timezone, timedelta
from dateutil.rrule import rrulestr
from dateutil.parser import parse
import calendar

class CalendarInterface (DataSourceInterface):
    """Interface for fetching and processing calendar event information."""
    def __init__ (self):
        self.events = self.__get_events__()
        self.events = self.__sort_events__(self.events)

    def __sort_events__ (self, events):
        events.sort(key=lambda x : x.begin_datetime)
        return events

    def __get_events__ (self):
        raise NotImplementedError("Functions needs to be implemented")

    def get_upcoming_events (self, timespan = None):
        if timespan is None:
            timespan = timedelta(31)
        return self.__get_events_in_range__(datetime.now(), timespan)

    def get_today_events (self):
        return self.get_day_events(datetime.now())

    def get_day_events (self, date):
        day_start = datetime(date.year, date.month, date.day)
        return self.__get_events_in_range__(day_start, timedelta(1))

    def get_month_events (self, month = -1):
        if month < 0:
            month = datetime.now().month
        
        month_start = datetime(datetime.now().year, month, 1)
        month_days = calendar.monthrange(month_start.year, month_start.month)[1]
        return self.__get_events_in_range__(month_start, timedelta(month_days))

    def get_week_events (self, week = -1):
        raise NotImplementedError("Support dropped. Needs update.")
        if week < 0 and week_starts_on == "Monday":
            week = int(datetime.now().strftime('%W')) + 1
        elif week < 0:
            week = int(datetime.now().strftime('%U')) + 1

        if week_starts_on == "Monday":
            return self.__get_events_in_range__(lambda x : int(x.begin_datetime.strftime('%W')) + 1 == week or int(x.end_datetime.strftime('%W')) + 1 == week)
        else:
            return self.__get_events_in_range__(lambda x : int(x.begin_datetime.strftime('%U')) + 1 == week or int(x.end_datetime.strftime('%U')) + 1 == week)

    def __get_events_in_range__ (self, start, duration):
        if self.events is None:
            return []

        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)

        events_in_range = []
        for event in self.events:
            event_occurrence = self.__get_if_event_in_range__(event, start, duration)
            if event_occurrence:
                events_in_range.extend(event_occurrence)

        events_in_range = self.__sort_events__(events_in_range)
        return events_in_range

    def __get_if_event_in_range__ (self, event, start, duration):
        '''Returns list or None'''
        if event is None:
            return None

        if event.rrule is None:
            return self.__is_onetime_in_range__(event, start, duration)
        else:
            return self.__is_repeating_in_range__(event, start, duration)

    def __is_onetime_in_range__ (self, event, start, duration):
        if event.begin_datetime > start:
            first_start = start
            first_duration = duration
            second_start = event.begin_datetime
            second_duration = event.duration
        else:
            first_start = event.begin_datetime
            first_duration = event.duration
            second_start = start
            second_duration = duration

        event_end = event.begin_datetime + event.duration

        if (second_start - first_start) < first_duration:
            return [ event ]
        else:
            return None

    def __is_repeating_in_range__ (self, event, start, duration):
        end = start + duration
        occurrences = []

        r_string=event.rrule
        rule=rrulestr(r_string,dtstart=parse(str(event.begin_datetime)))
        for occurrence in rule:
            if occurrence - end > timedelta(0):
                return occurrences
            merged_event = self.__merge_event_data__(event, start=occurrence)
            if self.__is_onetime_in_range__(merged_event, start, duration):
                occurrences.append(merged_event)
        return occurrences

    def __merge_event_data__ (self, event, start = None):
        if start is not None:
            event.begin_datetime = start
            event.end_datetime = start + event.duration
        
        return event