from PanelDesign import PanelDesign
from Assets import colors
from settings import general_settings
import calendar as callib
from datetime import datetime, timedelta, date
from PIL import ImageDraw
from TextDesign import TextDesign
from DayHeaderDesign import DayHeaderDesign
from DayRowDesign import DayRowDesign
from RssPostListDesign import RssPostListDesign
from CryptoListDesign import CryptoListDesign
from settings import line_thickness
from math import ceil

todayheader_pos = (0, 0)
todayheader_size = (1, 0.25)
lines_thickness = line_thickness
infoarea_replacedrowscount = 3

dayrowsarea_ypos = todayheader_size[1]
dayrowsarea_height = 1 - todayheader_size[1]
dayrow_min_format = 50 / 384
dayrow_max_format = 70 / 384
rss_y_padding = 5
crypto_y_padding = 5


class DayListPanel (PanelDesign):
    """Overview that focuses on the current day and
    lists following days in a list below."""

    def __init__(self, size):
        super(DayListPanel, self).__init__(size)
        self.__day_rows__ = []
        self.__calc_dayrow_size__()
        self.__first_render__()

    def __first_render__(self):
        self.__draw_today_header__()
        self.__draw_day_rows__()

    def add_weather(self, weather):
        for row in self.__day_rows__:
            row.add_weather(weather)

    def add_calendar(self, calendar):
        for row in self.__day_rows__:
            row.add_calendar(calendar)

    def add_rssfeed(self, rss):
        for row in self.__day_rows__:
            row.add_rssfeed(rss)
        if general_settings["info-area"] is "rss":
            self.__day_rows__ = self.__day_rows__[:-infoarea_replacedrowscount]
            self.__draw_rss_infoarea__(rss)

    def add_crypto(self, crypto):
        if general_settings["info-area"] is "crypto":
            self.__draw_crypto_infoarea__(crypto)

    def add_tasks(self, tasks):
        pass

    def __draw_rss_infoarea__(self, rss):
        height = infoarea_replacedrowscount * \
            self.dayrow_size[1] * self.size[1] - rss_y_padding
        ypos = self.size[1] - height
        size = (self.size[0], height)
        pos = (0, ypos)

        design = RssPostListDesign(size, rss)
        design.pos = pos
        self.draw_design(design)

    def __draw_crypto_infoarea__(self, crypto):
        height = infoarea_replacedrowscount * \
            self.dayrow_size[1] * self.size[1] - crypto_y_padding
        ypos = self.size[1] - height
        size = (self.size[0], height)
        pos = (0, ypos)

        design = CryptoListDesign(size, crypto)
        acutal_height = design.get_estimated_height()
        design.pos = (pos[0], pos[1] + (height - acutal_height))
        self.draw_design(design)

        replaced_rows = ceil(
            acutal_height / (self.dayrow_size[1] * self.size[1]))
        self.__day_rows__ = self.__day_rows__[:-replaced_rows]

    def __draw_day_rows__(self):
        following_days = self.__get_following_days__()
        for i, date in enumerate(following_days):
            row = DayRowDesign(self.__abs_co__(self.dayrow_size), date)
            row.pos = self.__get_day_row_pos__(i)
            self.__day_rows__.append(row)

    def __get_day_row_pos__(self, i):
        ypos = self.size[1] * dayrowsarea_ypos
        down_shift = i * self.dayrow_size[1] * self.size[1]
        return (0, int(ypos + down_shift))

    def __calc_dayrow_size__(self):
        max_area_height = dayrowsarea_height * self.size[1]
        max_row_number = max_area_height / (dayrow_min_format * self.size[0])
        min_row_number = max_area_height / (dayrow_max_format * self.size[0])
        average_row_number = (max_row_number + min_row_number) / 2
        self.dayrow_count = round(average_row_number)
        row_height = max_area_height / self.dayrow_count
        self.dayrow_size = (1, row_height / self.size[1])

    def __get_following_days__(self):
        following_days = []
        for i in range(self.dayrow_count):
            following_days.append(date.today() + timedelta(days=i + 1))
        return following_days

    def __draw_today_header__(self):
        header = DayHeaderDesign(self.__abs_co__(
            todayheader_size), date.today())
        header.pos = self.__abs_co__(todayheader_pos)
        self.__day_rows__.append(header)

    def __draw_lines__(self):
        positions = []
        for i in range(len(self.__day_rows__)):
            positions.append(self.__get_day_row_pos__(i)[1])
        for ypos in positions:
            line_start = (0, ypos)
            line_end = (self.size[0], ypos)
            ImageDraw.Draw(self.__image__).line(
                [line_start, line_end], fill=colors["fg"], width=lines_thickness)

    def __finish_panel__(self):
        for design in self.__day_rows__:
            self.draw_design(design)
        self.__draw_lines__()

    def __abs_co__(self, coordinates):
        return (int(coordinates[0] * self.size[0]), int(coordinates[1] * self.size[1]))
