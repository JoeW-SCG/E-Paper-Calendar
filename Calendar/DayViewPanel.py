from PanelDesign import PanelDesign
from datetime import datetime, timedelta, date
from DayHeaderDesign import DayHeaderDesign
from HourListDesign import HourListDesign

header_size = (1, 0.2)
hourlist_size = (1, 1 - header_size[1])

class DayViewPanel (PanelDesign):
    """Overview that focuses on the current day and
    shows a timeline split into hours."""
    def __init__ (self, size):
        super(DayViewPanel, self).__init__(size)
        self.__first_render__()

    def __first_render__ (self):
        self.__init_header__()
        self.__init_hourlist__()

    def add_weather (self, weather):
        self.__header__.add_weather(weather)

    def add_calendar (self, calendar):
        allday_ev, timed_ev = self.__split_events__(calendar.get_today_events())
        self.__header__.add_events(allday_ev)
        self.__hourlist__.add_events(timed_ev)

    def add_rssfeed (self, rss):
        pass

    def add_taks (self, tasks):
        pass

    def __finish_panel__ (self):
        self.draw_design(self.__header__)
        self.draw_design(self.__hourlist__)

    def __init_header__ (self):
        self.__header__ = DayHeaderDesign(self.__abs_co__(header_size), date.today())
        self.__header__.pos = (0, 0)

    def __init_hourlist__ (self):
        self.__hourlist__ = HourListDesign(self.__abs_co__(hourlist_size), 6, 18)
        self.__hourlist__.pos = (0, self.__header__.size[1])

    def __abs_co__ (self, coordinates):
        return (int(coordinates[0] * self.size[0]),int(coordinates[1] * self.size[1]))

    def __split_events__ (self, events):
        allday_ev = []
        timed_ev = []

        for event in events:
            if event.allday:
                allday_ev.append(event)
            elif event.multiday:
                if self.__is_today__(event.begin_datetime):
                    today = date.today()
                    tzinfo = event.end_datetime.tzinfo
                    event.end_datetime = datetime(today.year, today.month, today.day, 0, 0, 0, 0, tzinfo) + timedelta(1)
                    event.duration = timedelta(0, 0, 0, 0, event.begin_datetime.minute, event.begin_datetime.hour)
                    timed_ev.append(event)
                elif self.__is_today__(event.end_datetime):
                    today = date.today()
                    tzinfo = event.begin_datetime.tzinfo
                    event.begin_datetime = datetime(today.year, today.month, today.day, 0, 0, 0, 0, tzinfo)
                    event.duration = timedelta(0, 0, 0, 0, event.end_datetime.minute, event.end_datetime.hour)
                    timed_ev.append(event)
                else:
                    allday_ev.append(event)
            else:
                timed_ev.append(event)
        return allday_ev, timed_ev

    def __is_today__ (self, dt):
        today = date.today()
        return dt.day == today.day and \
            dt.month == today.month and \
            dt.year == today.year