from PanelDesign import PanelDesign
from Assets import *
from settings import *
import calendar
from datetime import datetime, timedelta
from WeatherHeaderDesign import WeatherHeaderDesign
from PIL import ImageDraw
from TextDesign import TextDesign
from BoxDesign import BoxDesign
from EllipseDesign import EllipseDesign

weatherheadersize = (1,0.113)
seperatorplace = (0, 0.113)
monthplace = (0, 0.12)
monthboxsize = (1, 0.085)
daynumberboxsize = (0.143, 0.143)
dayhighlightboxsize = (0.143, 0.07)
daynumbersize = 25
monthtextsize = 40
monthovposition = (0, 0.23)
monthovsize = (1, 0.5)
weekdayrowpos = (0, 0.209)
weekrowboxsize = (1, 0.044)
weekdaytextsize = 18
weekrownameboxsize = (0.143, 0.044)

class MonthOvPanel (PanelDesign):
    """Overview that focuses on the current month and
    some additional information in the bottom."""
    def __init__ (self, size):
        super(MonthOvPanel, self).__init__(size)
        self.__first_render__()

    def __first_render__ (self):
        if week_starts_on == "Monday":
            calendar.setfirstweekday(calendar.MONDAY)
        elif week_starts_on == "Sunday":
            calendar.setfirstweekday(calendar.SUNDAY)

        self.__draw_month_name__()
        self.__draw_seperator__()
        self.__draw_month_overview__()
        self.__draw_week_row__()

    def add_weather (self, weather):
        self.draw_design(WeatherHeaderDesign(self.__abs_pos__(weatherheadersize), weather))

    def add_calendar (self, calendar):
        raise NotImplementedError("Functions needs to be implemented")

    def add_rssfeed (self, rss):
        raise NotImplementedError("Functions needs to be implemented")

    def __abs_pos__ (self, pos, size = None):
        if size is None:
            size = self.size
        return (int(pos[0] * size[0]), int(pos[1] * size[1]))

    def __draw_seperator__ (self):
        """Draw a line seperating the weather and Calendar section"""
        ImageDraw.Draw(self.__image__).line([ self.__abs_pos__(seperatorplace), self.__abs_pos__((1, seperatorplace[1])) ], fill='red', width=5)

    def __draw_day_number__ (self, number, pos):
        if number <= 0:
            return
        txt = TextDesign(self.__abs_pos__(daynumberboxsize), fontsize=daynumbersize, text=str(number), verticalalignment="center", horizontalalignment="center")
        txt.pos = pos
        self.draw_design(txt)

    def __draw_month_name__ (self):
        """Draw the icon with the current month's name"""
        month = datetime.now().strftime("%B")
        txt = TextDesign(self.__abs_pos__(monthboxsize), fontsize=monthtextsize, text=month, verticalalignment="center", horizontalalignment="center")
        txt.pos = self.__abs_pos__(monthplace)
        self.draw_design(txt)

    def __get_day_pos__ (self, week_in_month, day_of_week):
        maxwidth, maxheight = self.__abs_pos__(monthovsize)
        partialwidth = maxwidth / 7
        partialheight = maxheight / 5
        posx, posy = self.__abs_pos__(monthovposition)
        return (int(posx + day_of_week * partialwidth), int(posy + week_in_month * partialheight))

    def __draw_month_overview__ (self):
        """Using the built-in calendar function, draw icons for each
            number of the month (1,2,3,...28,29,30)"""
        cal = calendar.monthcalendar(datetime.now().year, datetime.now().month)
        for week in cal:
            for numbers in week:
                self.__draw_day_number__(numbers, self.__get_day_pos__(cal.index(week), week.index(numbers)))

        self.__draw_highlight_box__(self.__abs_pos__(dayhighlightboxsize), self.__get_today_box_pos__(), width=3)

    def __draw_week_row__ (self):
        week_days = self.__get_week_days_ordered__()

        for day_of_week, day in enumerate(week_days):
            txt = TextDesign(self.__abs_pos__(weekrownameboxsize), fontsize=weekdaytextsize, text=str(day), verticalalignment="center", horizontalalignment="center")
            txt.pos = self.__get_week_day_pos__(day_of_week)
            self.draw_design(txt)
        
        self.__draw_highlight_box__(self.__abs_pos__(weekrownameboxsize), self.__get_week_day_pos__(datetime.now().weekday()), width=1)

    def __get_week_day_pos__ (self, day_of_week):
        maxwidth, _ = self.__abs_pos__(monthovsize)
        partialwidth = maxwidth / 7
        posx, posy = self.__abs_pos__(weekdayrowpos)
        return (int(posx + day_of_week * partialwidth), int(posy))

    def __get_today_box_pos__ (self):
        x, y = self.__get_day_pos__(int(datetime.now().day / 7), datetime.now().weekday())
        return (x, int(y + (self.__abs_pos__(daynumberboxsize)[1] - self.__abs_pos__(dayhighlightboxsize)[1]) / 2))

    def __draw_highlight_box__ (self, size, pos, color='black', width=1):
        design = BoxDesign(size, outline=color, width = width)
        design.pos = pos
        self.draw_design(design)

    def __draw_highlight_circle__ (self, size, pos, color = 'black', width=1):
        design = EllipseDesign(size, outline=color, width = width)
        design.pos = pos
        self.draw_design(design)

    def __get_week_days_ordered__ (self):
        cur_weekday = datetime.now().weekday()
        correction = -cur_weekday
        if week_starts_on == "Sunday":
            correction -= 1

        weekdays = []
        for i in range(7):
            weekdays.append((datetime.now() + timedelta(days=(i + correction))).strftime("%a"))

        return weekdays