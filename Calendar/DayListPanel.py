from PanelDesign import PanelDesign
from Assets import *
from settings import *
import calendar
from datetime import datetime, timedelta
from PIL import ImageDraw
from TextDesign import TextDesign
from BoxDesign import BoxDesign
from EllipseDesign import EllipseDesign
from DayHeaderDesign import DayHeaderDesign

todayheader_pos = (0,0)
todayheader_size = (1,0.25)
headerline_color = "black"
lines_thickness = 1

class DayListPanel (PanelDesign):
    """Overview that focuses on the current day and
    lists following days in a list below."""
    def __init__ (self, size):
        super(DayListPanel, self).__init__(size)
        self.__first_render__()
        self.__day_rows__ = []

    def __first_render__ (self):
        if week_starts_on == "Monday":
            calendar.setfirstweekday(calendar.MONDAY)
        elif week_starts_on == "Sunday":
            calendar.setfirstweekday(calendar.SUNDAY)

        self.__draw_today_header__()

    def add_weather (self, weather):
        pass

    def add_calendar (self, calendar):
        pass

    def add_rssfeed (self, rss):
        pass

    def __draw_today_header__ (self):
        header = DayHeaderDesign(self.__abs_co__(todayheader_size), datetime.now())
        header.pos = self.__abs_co__(todayheader_pos)
        self.draw_design(header)

        line_start = (0, self.__abs_co__(todayheader_size)[1])
        line_end = self.__abs_co__(todayheader_size)
        ImageDraw.Draw(self.__image__).line([line_start, line_end], fill=headerline_color, width=lines_thickness)

    def __abs_co__(self, coordinates):
        return (int(coordinates[0] * self.size[0]),int(coordinates[1] * self.size[1]))