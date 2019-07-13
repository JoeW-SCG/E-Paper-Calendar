from CalendarInterface import CalendarInterface
from CalendarEvent import CalendarEvent
from ics import Calendar
from datetime import datetime, timedelta, timezone
import re
from settings import week_starts_on
from urllib.request import urlopen


class IcalEvents(CalendarInterface):
    """Fetches events from ical addresses."""

    def __init__(self, urls, highlighted_urls=None):
        self.urls = urls
        self.highlighted_urls = highlighted_urls
        super(IcalEvents, self).__init__()

    def is_available(self):
        for url in self.urls + self.highlighted_urls:
            try:
                urlopen(url)
                return True
            except:
                pass
        return False

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

        if urls is None:
            return loaded_events

        for calendar in urls:
            try:
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

                    cal_event.begin_datetime = cal_event.begin_datetime.astimezone(
                        None)
                    cal_event.end_datetime = cal_event.end_datetime.astimezone(
                        None)

                    if cal_event.allday:
                        cal_event = self.__fix_allday__(cal_event)

                    cal_event.multiday = self.__is_multiday__(cal_event)

                    loaded_events.append(cal_event)
            except BaseException as ex:
                print("ICal-Error [" + calendar + "]")
                print(ex)
        return loaded_events

    def __fix_allday__(self, event):
        local_tzinfo = datetime.now(timezone.utc).astimezone().tzinfo
        begin_utc = event.begin_datetime.astimezone(timezone.utc)
        end_utc = event.end_datetime.astimezone(timezone.utc)

        event.begin_datetime = datetime(
            begin_utc.year, begin_utc.month, begin_utc.day, 0, 0, 0, 0, local_tzinfo)
        event.end_datetime = datetime(
            end_utc.year, end_utc.month, end_utc.day, 0, 0, 0, 0, local_tzinfo) - timedelta(1)
        event.duration = event.end_datetime - event.begin_datetime

        return event

    def __remove_alarms__(self, decode):
        alarm_begin = 'BEGIN:VALARM'
        alarm_end = 'END:VALARM'
        lineseparation = '\r\n'

        beginAlarmIndex = 0
        while beginAlarmIndex >= 0:
            beginAlarmIndex = decode.find(alarm_begin)
            if beginAlarmIndex >= 0:
                endAlarmIndex = decode.find(alarm_end, beginAlarmIndex)
                decode = decode[:beginAlarmIndex] + \
                    decode[endAlarmIndex +
                           len(alarm_end) + len(lineseparation):]
        return decode

    def __extract_rrule__(self, event):
        if re.search('RRULE', str(event)) is None:
            return None

        return re.search('RRULE:(.+?)\n', str(event)).group(1).rstrip()

    def __is_multiday__(self, event):
        if event.allday and event.duration == timedelta(1):
            return False

        return event.begin_datetime.day != event.end_datetime.day or \
            event.begin_datetime.month != event.end_datetime.month or \
            event.begin_datetime.year != event.end_datetime.year
