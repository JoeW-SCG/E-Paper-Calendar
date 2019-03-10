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
        super(IcalEvents, self).__init__()

    def __get_events__(self):
        loaded_events = []
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
                    cal_event.allday = event.all_day

                    loaded_events.append(cal_event)
            return loaded_events
        except:
            return []

    def __fix_errors__(self, decode):
        return decode.replace('BEGIN:VALARM\r\nACTION:NONE','BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:') \
               .replace('BEGIN:VALARM\r\nACTION:EMAIL','BEGIN:VALARM\r\nACTION:DISPLAY\r\nDESCRIPTION:')