from PanelDesign import PanelDesign
from Assets import *
from settings import *
import calendar
from datetime import datetime
from WeatherHeaderDesign import WeatherHeaderDesign
from PIL import ImageDraw
from TextDesign import TextDesign

weatherheadersize = (1,0.113)
seperatorplace = (0, 0.113)
monthplace = (0, 0.116)
weekplace = (0, 0.209)
monthboxsize = (1, 0.085)
daynumberboxsize = (0.143, 0.143)
daynumbersize = 28
monthtextsize = 40
monthovposition = (0, 0.225)
monthovsize = (1, 0.5)

class MonthOvPanel (PanelDesign):
    """Overview that focuses on the current month and
    some additional information in the bottom."""
    def __init__ (self, size):
        super(MonthOvPanel, self).__init__(size)
        self.__first_render__()

    def __first_render__ (self):
        time = datetime.now()

        self.__draw_month_name__()
        self.__draw_seperator__()
        """Draw the icons with the weekday-names (Mon, Tue...) and
            draw a circle  on the current weekday"""
        #if (week_starts_on == "Monday"):
        #    calendar.setfirstweekday(calendar.MONDAY)
        #    self.draw(weekmon, self.__abs_pos__(weekplace))
        #    self.draw_bitmap(weekday, weekdaysmon[(time.strftime("%a"))])
        #elif (week_starts_on == "Sunday"):
        #    calendar.setfirstweekday(calendar.SUNDAY)
        #    self.draw(weeksun, self.__abs_pos__(weekplace))
        #    self.draw_bitmap(weekday, weekdayssun[(time.strftime("%a"))])
        """Using the built-in calendar function, draw icons for each
            number of the month (1,2,3,...28,29,30)"""
        cal = calendar.monthcalendar(time.year, time.month)
        for week in cal:
            for numbers in week:
                self.__draw_day_number__(numbers, self.__get_day_pos__(cal.index(week), week.index(numbers)))
    
    def add_weather (self, weather):
        self.draw_design(WeatherHeaderDesign(self.__abs_pos__(weatherheadersize), weather))

    def add_calendar (self, calendar):
        raise NotImplementedError("Functions needs to be implemented")

    def add_rssfeed (self, rss):
        raise NotImplementedError("Functions needs to be implemented")

    def __abs_pos__(self, pos):
        return (int(pos[0] * self.size[0]), int(pos[1] * self.size[1]))

    def __draw_seperator__(self):
        """Draw a line seperating the weather and Calendar section"""
        ImageDraw.Draw(self.__image__).line( [self.__abs_pos__(seperatorplace), self.__abs_pos__((1, seperatorplace[1]))], fill='red', width=5)

    def __draw_day_number__(self, number, pos):
        if number <= 0:
            return
        txt = TextDesign(self.__abs_pos__(daynumberboxsize), fontsize=daynumbersize, text=str(number), verticalalignment="center", horizontalalignment="center")
        txt.pos = pos
        self.draw_design(txt)

    def __draw_month_name__(self):
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
        return (posx + day_of_week * partialwidth, posy + week_in_month * partialheight)