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
        self.__add_allday_events__(calendar)
        self.__add_timed_events__(calendar)

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

    def __add_allday_events__ (self, calendar):
        allday_events = [event for event in calendar.get_today_events() if event.allday]
        self.__header__.add_events(allday_events)

    def __add_timed_events__ (self, calendar):
        timed_events = [event for event in calendar.get_today_events() if event.allday is False]
        self.__hourlist__.add_events(timed_events)

    def __abs_co__ (self, coordinates):
        return (int(coordinates[0] * self.size[0]),int(coordinates[1] * self.size[1]))