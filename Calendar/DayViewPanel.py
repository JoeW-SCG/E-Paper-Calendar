from PanelDesign import PanelDesign
from datetime import datetime, timedelta, date
from DayHeaderDesign import DayHeaderDesign
from HourListDesign import HourListDesign
from settings import general_settings
from RssPostListDesign import RssPostListDesign
from PIL import ImageDraw
from Assets import colors
from EventListDesign import EventListDesign
from CryptoListDesign import CryptoListDesign


header_size = (1, 0.2)
hourlist_size = (1, 1 - header_size[1])
default_shownhours_count = 12

infoarea_replaced_hours = 4
infoarea_borderline_width = 1
infoarea_padding = 5

class DayViewPanel (PanelDesign):
    """Overview that focuses on the current day and
    shows a timeline split into hours."""
    def __init__ (self, size):
        super(DayViewPanel, self).__init__(size)
        self.shownhours_count = default_shownhours_count
        if general_settings["info-area"] not in ["", "empty"]:
            self.shownhours_count -= infoarea_replaced_hours
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

        if general_settings["info-area"] == "events":
            self.__draw_event_list__(calendar)
            self.__draw_infoarea_line__()

    def add_rssfeed (self, rss):
        if general_settings["info-area"] == "rss":
            self.__draw_rss_feed__(rss)
            self.__draw_infoarea_line__()

    def add_cryptofeed (self, crypto):
        if general_settings["info-area"] == "crypto":
            self.__draw_crypto_feed__(crypto)
            self.__draw_infoarea_line__()

    def __draw_infoarea_line__(self):
        height = infoarea_replaced_hours * self.__hourlist__.row_size[1]
        ypos = self.size[1] - height

        line_start = (0, ypos)
        line_end = (self.size[0], ypos)
        ImageDraw.Draw(self.__image__).line([ line_start, line_end ], fill=colors["fg"], width=infoarea_borderline_width)

    def __draw_rss_feed__(self, rss):
        height = infoarea_replaced_hours * self.__hourlist__.row_size[1] - infoarea_padding
        size = (self.size[0], height)
        pos = (0, self.size[1] - size[1])

        rss = RssPostListDesign(size, rss)
        rss.pos = pos
        self.draw_design(rss)

    def __draw_crypto_feed__(self, crypto):
        height = infoarea_replaced_hours * self.__hourlist__.row_size[1] - infoarea_padding
        size = (self.size[0], height)
        pos = (0, self.size[1] - size[1])

        crypto = CryptoListDesign(size, crypto)
        crypto.pos = pos
        self.draw_design(crypto)


    def __draw_event_list__(self, calendar):
        height = infoarea_replaced_hours * self.__hourlist__.row_size[1] - infoarea_padding
        size = (self.size[0], height)
        pos = (0, self.size[1] - size[1])

        events = EventListDesign(size, calendar.get_upcoming_events())
        events.pos = pos
        self.draw_design(events)

    def add_taks (self, tasks):
        pass

    def __finish_panel__ (self):
        self.draw_design(self.__header__)
        self.draw_design(self.__hourlist__)

    def __init_header__ (self):
        self.__header__ = DayHeaderDesign(self.__abs_co__(header_size), date.today())
        self.__header__.pos = (0, 0)

    def __init_hourlist__ (self):
        start, end = self.__get_current_hour_range__()
        size = self.__abs_co__(hourlist_size)
        size = (size[0], size[1] * self.shownhours_count / default_shownhours_count)

        self.__hourlist__ = HourListDesign(size, start, end)
        self.__hourlist__.pos = (0, self.__header__.size[1])

    def __get_current_hour_range__(self):
        start_hour = datetime.now().hour
        additional_hours = self.shownhours_count - 1

        if start_hour + additional_hours > 23:
            start_hour = 23 - additional_hours

        return start_hour, start_hour + additional_hours

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
                    timed_ev.append(event)
                elif self.__is_today__(event.end_datetime):
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
