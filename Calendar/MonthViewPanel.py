from PanelDesign import PanelDesign
from settings import general_settings, week_starts_on
from PIL import ImageDraw
from datetime import date
from Assets import colors
import calendar as callib
from TableDesign import TableDesign
from DayBoxDesign import DayBoxDesign
from RssPostListDesign import RssPostListDesign
from WeatherHeaderDesign import WeatherHeaderDesign

weather_height = 0.113
info_height = 0.25
info_padding = 5
seperator_width = 3

class MonthViewPanel (PanelDesign):
    """Displays a grid of the day of the current month
    with detailed event descriptions."""
    def __init__(self, size, month = None, year = None):
        super(MonthViewPanel, self).__init__(size)
        self.day_table = []
        self.month = month
        if self.month == None:
            self.month = date.today().month
        self.year = year
        if self.year == None:
            self.year = date.today().year
        self.__init_sizes__()
        self.__init_day_boxes__()

    def __init_sizes__(self):
        self.weather_height = 0
        self.info_height = 0
        if general_settings["info-area"] in ["events", "rss"]:
            self.info_height = info_height
        if general_settings["weather-info"]:
            self.weather_height = weather_height
        self.day_area_height = 1 - self.weather_height - self.info_height
        self.day_area_ypos = self.weather_height

        area_height = self.size[1] * self.day_area_height
        area_width = self.size[0]
        self.day_box_size = (area_width / 7, area_height)

    def add_weather (self, weather):
        if general_settings["weather-info"] == False:
            return
        size = (self.size[0], self.size[1] * self.weather_height)

        header = WeatherHeaderDesign(size, weather)
        self.draw_design(header)
        self.__draw_seperator__(size[1], colors["hl"])

    def add_calendar (self, calendar):
        self.__add_calendar_to_days__(calendar)

    def __add_calendar_to_days__(self, calendar):
        for week in self.day_table:
            for day in week:
                if day != None:
                    day.add_calendar(calendar)

    def add_rssfeed (self, rss):
        if general_settings["info-area"] != "rss":
            return

        size = (self.size[0], self.size[1] * self.info_height)
        pos = (0, self.size[1] - size[1] + info_padding)

        rss = RssPostListDesign(size, rss)
        rss.pos = pos
        self.draw_design(rss)

    def add_taks (self, tasks):
        pass

    def __finish_panel__(self):
        self.__draw_days__()

    def __draw_days__(self):
        size = (self.size[0], self.size[1] * self.day_area_height)
        pos = (0, self.size[0] * self.day_area_ypos)

        table = TableDesign(size, matrix = self.day_table)
        table.pos = pos
        self.draw_design(table)

    def __draw_seperator__ (self, height, color):
        ImageDraw.Draw(self.__image__).line([ (0, height * self.size[1]), (self.size[0], height * self.size[1]) ], fill=color, width=seperator_width)

    def __init_day_boxes__(self):
        if week_starts_on == "Monday":
            callib.setfirstweekday(callib.MONDAY)
        elif week_starts_on == "Sunday":
            callib.setfirstweekday(callib.SUNDAY)

        weeks = callib.monthcalendar(self.year, self.month)
        for i, week in enumerate(weeks):
            self.day_table.append([])
            for day in week:
                self.day_table[i].append(self.__create_day__(day))

    def __create_day__(self, day):
        if day == None or day == 0:
            return None

        design = DayBoxDesign(self.day_box_size, date(self.year, self.month, int(day)))

        return design