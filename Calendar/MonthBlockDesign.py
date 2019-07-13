from DesignEntity import DesignEntity
import calendar as callib
from datetime import datetime, timedelta
from TextDesign import TextDesign
from Assets import colors
from settings import week_starts_on
from BoxDesign import BoxDesign

daynumberboxsize = (0.143, 0.2)
dayhighlightboxsize = (0.143, 0.14)
daynumbersize = daynumberboxsize[0] * 0.45
day_number_ypadding = -0.002


class MonthBlockDesign (DesignEntity):
    """Creates a view containing one week of the month in
    one row"""

    def __init__(self, size, datetime_month, highlight_today=False):
        super(MonthBlockDesign, self).__init__(size, mask=True)
        self.month = datetime_month.month
        self.year = datetime_month.year
        self.highlight_today = highlight_today
        self.__week_days__ = self.__get_week_days_ordered__()

    def __finish_image__(self):
        self.__draw_month_overview__()

    def __draw_month_overview__(self):
        """Using the built-in calendar function, draw icons for each
            number of the month (1,2,3,...29,30,31)"""
        cal = callib.monthcalendar(self.year, self.month)
        for week in cal:
            for numbers in week:
                self.__draw_day_number__(numbers, self.get_day_pos(
                    cal.index(week), week.index(numbers)))

        if self.highlight_today:
            self.__draw_highlight_box__(self.__abs_pos__(
                dayhighlightboxsize), self.__get_today_box_pos__(), width=3)

    def __draw_highlight_box__(self, size, pos, color=colors["fg"], width=1):
        design = BoxDesign(size, outline=color, width=width)
        design.pos = pos
        self.draw_design(design)

    def __draw_day_number__(self, number, pos):
        if number <= 0:
            return
        txt = TextDesign(self.__abs_pos__(daynumberboxsize), fontsize=daynumbersize *
                         self.size[0], text=str(number), verticalalignment="center", horizontalalignment="center")
        txt.pos = (pos[0], pos[1] + day_number_ypadding * self.size[1])
        self.draw_design(txt)

    def get_day_pos(self, week_in_month, day_of_week, rel_pos=(0, 0)):
        maxwidth, maxheight = self.size
        partialwidth = maxwidth / 7
        partialheight = maxheight / 5
        return (int(rel_pos[0] + day_of_week * partialwidth), int(rel_pos[1] + week_in_month * partialheight))

    def __get_today_box_pos__(self):
        x, y = self.get_day_pos(self.__get_week_of_month__(
            datetime.now()), self.__get_day_of_week__(datetime.now()))
        return (x, int(y + (self.__abs_pos__(daynumberboxsize)[1] - self.__abs_pos__(dayhighlightboxsize)[1]) / 2))

    def __get_week_of_month__(self, date):
        for wof, week in enumerate(callib.monthcalendar(date.year, date.month)):
            if date.day in week:
                return wof
        return 0

    def __get_day_of_week__(self, date):
        return self.__week_days__.index(date.strftime("%a"))

    def __get_week_days_ordered__(self):
        cur_weekday = datetime.now().weekday()
        correction = -cur_weekday
        if week_starts_on == "Sunday":
            correction -= 1

        weekdays = []
        for i in range(7):
            weekdays.append(
                (datetime.now() + timedelta(days=(i + correction))).strftime("%a"))

        return weekdays

    def __abs_pos__(self, pos, size=None):
        if size is None:
            size = self.size
        return (int(pos[0] * size[0]), int(pos[1] * size[1]))

    def get_real_height(self):
        weeks_in_month = callib.monthcalendar(self.year, self.month)
        num_size = self.__abs_pos__(daynumberboxsize)
        num_pos = self.get_day_pos(len(weeks_in_month) - 1, 6)
        return num_size[1] + num_pos[1]
