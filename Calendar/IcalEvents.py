from CalendarInterface import CalendarInterface
from CalendarEvent import CalendarEvent
from ics import Calendar
from datetime import datetime, timedelta, timezone
import re
from settings import week_starts_on
try:
    from urllib.request import urlopen
except Exception as e:
    print("Something didn't work right, maybe you're offline?" + e.reason)

class IcalEvents(CalendarInterface):
    """Fetches events from ical addresses."""
    def __init__(self, urls, highlighted_urls=None):
        self.urls = urls
        self.highlighted_urls = highlighted_urls
        super(IcalEvents, self).__init__()

    def __get_events__(self):
        events = self.__get_events_from_urls__(self.urls)

        highlighted = self.__get_events_from_urls__(self.highlighted_urls)
        highlighted = map(self.__highlight_event__, highlighted)
        events.extend(highlighted)

        return events

    def __highlight_event__(self, event):
        event.highlight = True
        return event

    def __get_events_from_urls__(self, urls):
        loaded_events = []
        try:
            if urls is None:
                return loaded_events

            for calendar in urls:
                decode = str(urlopen(calendar).read().decode())
                decode = self.__remove_alarms__(decode)

                ical = Calendar(decode)
                for event in ical.events:
                    cal_event = CalendarEvent()

                    cal_event.fetch_datetime = datetime.now(timezone.utc)
                    cal_event.begin_datetime = event.begin.datetime
                    cal_event.end_datetime = event.end.datetime
                    cal_event.duration = event.duration
                    cal_event.title = event.name
                    cal_event.description = event.description
                    cal_event.location = event.location
                    cal_event.allday = event.all_day
                    cal_event.rrule = self.__extract_rrule__(event)

                    if cal_event.allday:
                        cal_event.end_datetime =  cal_event.end_datetime - timedelta(1)
                        cal_event.duration = cal_event.duration - timedelta(1)

                    loaded_events.append(cal_event)
            return loaded_events
        except BaseException as ex:
            print("ICal-Error [" + calendar + "]")
            print(ex)
            return loaded_events

    def __remove_alarms__(self, decode):
        alarm_begin = 'BEGIN:VALARM'
        alarm_end = 'END:VALARM'
        lineseparation = '\r\n'

        beginAlarmIndex = 0
        while beginAlarmIndex >= 0:
            beginAlarmIndex = decode.find(alarm_begin)
            if beginAlarmIndex >= 0:
                endAlarmIndex = decode.find(alarm_end, beginAlarmIndex)
                decode = decode[:beginAlarmIndex] + decode[endAlarmIndex + len(alarm_end) + len(lineseparation):]
        return decode

    def __extract_rrule__(self, event):
        if re.search('RRULE',str(event)) is None:
            return None

        return re.search('RRULE:(.+?)\n',str(event)).group(1).rstrip()