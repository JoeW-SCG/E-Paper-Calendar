from CalendarInterface import CalendarInterface
from CalendarEvent import CalendarEvent
from ics import Calendar
from datetime import datetime, timedelta, timezone
from settings import week_starts_on
try:
    from urllib.request import urlopen
except Exception as e:
    print("Something didn't work right, maybe you're offline?" + e.reason)

class IcalEvents(CalendarInterface):
    """Fetches events from ical addresses."""
    def __init__(self, urls):
        self.urls = urls
        self.__load_events_from_urls__()

    def __load_events_from_urls__(self):
        self.loaded_events = []
        try:
            for calendar in self.urls:
                decode = str(urlopen(calendar).read().decode())
                fixed_decode = self.__fix_errors__(decode)

                ical = Calendar(fixed_decode)
                for event in ical.events:
                    cal_event = CalendarEvent()

                    cal_event.fetch_datetime = datetime.now()
                    cal_event.begin_datetime = event.begin.datetime
                    cal_event.end_datetime = event.end.datetime
                    cal_event.title = event.name
                    cal_event.description = event.description
                    cal_event.location= event.location

                    self.loaded_events.append(cal_event)
        except:
            return

    def __fix_errors__(self, decode):
        return decode.replace('BEGIN:VALARM\r\nACTION:NONE','BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:') \
               .replace('BEGIN:VALARM\r\nACTION:EMAIL','BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:')

    def get_upcoming_events(self):
        return self.__get_events_to_filter__(lambda x : (x.begin_datetime - datetime.now(timezone.utc)) > timedelta(0))

    def get_today_events(self):
        return self.get_day_events(datetime.now(timezone.utc))

    def get_day_events(self, date):
        return self.__get_events_to_filter__(lambda x : x.begin_datetime.strftime('%d-%m-%y') == date.strftime('%d-%m-%y'))

    def get_month_events(self, month = -1):
        if month < 0:
            month = datetime.now().month
        return self.__get_events_to_filter__(lambda x : x.begin_datetime.month == month)

    def get_week_events(self, week = -1):
        raise NotImplementedError("Malfunctioning")
        if week_starts_on == "Monday":
            return self.__get_events_to_filter__(lambda x : int(x.begin_datetime.strftime('%W')) + 1 == week)
        else:
            return self.__get_events_to_filter__(lambda x : int(x.begin_datetime.strftime('%U')) + 1 == week)

    def __get_events_to_filter__(self, event_filter):
        return [event for event in self.loaded_events if event_filter(event)]