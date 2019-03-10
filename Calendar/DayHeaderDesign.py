from DesignEntity import DesignEntity
from PIL import ImageDraw
from TextDesign import TextDesign
from WeatherColumnDesign import WeatherColumnDesign
from datetime import date, timedelta
from SingelDayEventListDesign import SingelDayEventListDesign

numberbox_ypos = 0.15
numberbox_height = 1 - 2 * numberbox_ypos
number_height = numberbox_height * 0.83
month_height = numberbox_height / 4
monthbox_xpadding = 0.013
monthbox_width = 1 - numberbox_ypos - monthbox_xpadding
weekday_height = numberbox_height * 0.22
weekday_ypadding = 0.02
weathercolumn_y_size = (0.4, 1)
eventlist_y_fontsize = 0.093
eventlist_padding = monthbox_xpadding

numberbox_font_color = "white"
numberbox_background_color = "red"
general_text_color = "black"
background_color = "white"
highlight_color = "red"

class DayHeaderDesign (DesignEntity):
    """Detailed and big view of a given date."""
    def __init__ (self, size, date):
        super(DayHeaderDesign, self).__init__(size)
        self.__init_image__(color=background_color)
        self.date = date

    def add_weather (self, weather):
        forecast = weather.get_forecast_in_days(self.date.day - date.today().day)
        size = (weathercolumn_y_size[0] * self.size[1], weathercolumn_y_size[1] * self.size[1])
        pos = (self.size[0] - size[0], 0)

        design = WeatherColumnDesign(size, forecast)
        design.pos = pos
        self.draw_design(design)

    def add_calendar (self, calendar):
        self.__draw_event_list__(calendar)

    def add_rssfeed (self, rss):
        pass

    def __finish_image__ (self):
        self.__draw_number_square__()
        self.__draw_month__()
        self.__draw_weekday__()

    def __draw_event_list__ (self, calendar):
        box_ypos = numberbox_ypos * self.size[1]
        box_xpos = numberbox_ypos * self.size[1]
        box_height = numberbox_height * self.size[1]
        padding = eventlist_padding * self.size[0]
        month_height = weekday_height * self.size[1]
        weather_width = weathercolumn_y_size[0] * self.size[1]
        pos = (box_xpos + box_height + padding, box_ypos + month_height + padding)
        size = (self.size[0] - pos[0] - weather_width, self.size[1] - pos[1] - box_ypos)
        fontsize = eventlist_y_fontsize * self.size[1]

        event_list = SingelDayEventListDesign(size, calendar, self.date, fontsize, general_color=general_text_color, background_color=background_color, highlight_color=highlight_color)
        event_list.pos = pos
        self.draw_design(event_list)

    def __draw_weekday__ (self):
        font_size = int(weekday_height * self.size[1])
        padding = int(weekday_ypadding * self.size[1])
        box_ypos = int((numberbox_ypos) * self.size[1]) + padding
        box_xpos = int(numberbox_ypos * self.size[1])
        box_height = int((1 - numberbox_ypos - numberbox_height) * self.size[1])
        box_pos = (box_xpos, box_ypos)
        box_size = (int(numberbox_height * self.size[1]), box_height)
        
        week_day_name = self.date.strftime("%A")
        week_day = TextDesign(box_size, text=week_day_name, background_color=numberbox_background_color, color=numberbox_font_color, fontsize=font_size, horizontalalignment="center")
        week_day.pos = box_pos
        self.draw_design(week_day)

    def __draw_month__ (self):
        font_size = int(month_height * self.size[1])
        padding = int(monthbox_xpadding * self.size[0])
        box_ypos = int(numberbox_ypos * self.size[1])
        box_height = int(numberbox_height * self.size[1])
        box_pos = (box_ypos + box_height + padding, box_ypos)
        box_size = (int(monthbox_width * self.size[0]), box_height)
        
        month_name = self.date.strftime("%B")
        month = TextDesign(box_size, text=month_name, fontsize=font_size, color=general_text_color, background_color=background_color)
        month.pos = box_pos
        self.draw_design(month)

    def __draw_number_square__ (self):
        box_ypos = int(numberbox_ypos * self.size[1])
        box_height = int(numberbox_height * self.size[1])
        box_topleft = (box_ypos,box_ypos)
        box_bottomright = (box_topleft[0] + box_height, box_topleft[1] + box_height)
        ImageDraw.Draw(self.__image__).rectangle([ box_topleft, box_bottomright ], fill=numberbox_background_color)

        font_size = int(number_height * self.size[1])
        box_size = (box_height, box_height)
        day_text = self.__get_day_text__()
        number = TextDesign(box_size, text=day_text, background_color=numberbox_background_color, color=numberbox_font_color, fontsize=font_size, horizontalalignment="center", verticalalignment="center")
        number.pos = box_topleft
        self.draw_design(number)

    def __abs_co__ (self, coordinates):
        return (int(coordinates[0] * self.size[0]),int(coordinates[1] * self.size[1]))

    def __get_day_text__ (self):
        if self.date.strftime("%d-%m") is "14-03": #PI-Day
            return "π"
        return str(self.date.day)