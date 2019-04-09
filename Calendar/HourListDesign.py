from DesignEntity import DesignEntity
from settings import hours, language
from TextDesign import TextDesign
from PIL import ImageDraw
from Assets import colors, defaultfontsize
from BoxDesign import BoxDesign

hourbox_y_width = 1
hour_box_fontsize = 0.75
hoursubtext_fontsize = 0.7
hoursubtext_height = 0.35
event_title_fontsize = defaultfontsize
event_title_padding = 1
line_thickness = 1

class HourListDesign (DesignEntity):
    """Hours of a day are listed vertically and
    resemble a timeline."""
    def __init__ (self, size, first_hour = 0, last_hour = 23):
        super(HourListDesign, self).__init__(size)
        self.first_hour = first_hour
        self.last_hour = last_hour
        self.events = []

    def add_events (self, events):
        self.events.extend(events)

    def __finish_image__ (self):
        self.__calc_parameters__()
        self.__draw_hour_rows__()
        self.__draw_lines__()
        
        for event in self.events:
            self.__draw_event__(event)

    def __calc_parameters__ (self):
        self.hour_count = self.last_hour - self.first_hour + 1
        self.__row_size__ = (self.size[0], self.size[1] / self.hour_count)
        self.number_columns = 1

    def __get_hour_text__ (self, hour):
        if hour <= 12 or hours is "24":
            return str(hour)
        else:
            short = hour - 12
            return str(short) if short > 0 else "12"

    def __get_ypos_for_time__ (self, hour, minute = 0):
        return self.__get_height_for_duration__(hour, minute) - self.__get_height_for_duration__(self.first_hour)

    def __get_height_for_duration__ (self, hours, minutes = 0):
        row_height = self.__row_size__[1]
        return row_height * (hours + minutes / 60)

    def __draw_hour_rows__ (self):
        for hour in range(self.first_hour, self.last_hour + 1):
            self.__draw_row__(hour)

    def __draw_row__ (self, hour):
        subtext_height = self.__row_size__[1] * hoursubtext_height
        sub_fontsize = subtext_height * hoursubtext_fontsize
        width = hourbox_y_width * self.__row_size__[1]
        height = self.__row_size__[1] - subtext_height
        size = (width, height)
        pos = (0, self.__get_ypos_for_time__(hour))
        fontsize = size[1] * hour_box_fontsize

        txt = TextDesign(size, text=self.__get_hour_text__(hour), fontsize=fontsize, verticalalignment="bottom", horizontalalignment="center")
        txt.pos = pos
        self.draw_design(txt)

        sub = TextDesign((width, subtext_height), text=self.__get_hour_sub_text__(hour), fontsize=sub_fontsize, verticalalignment="top", horizontalalignment="center")
        sub.pos = (0, height + self.__get_ypos_for_time__(hour))
        self.draw_design(sub)

    def __draw_lines__ (self):
        for i in range(self.hour_count):
            ypos = i * self.__row_size__[1]
            line_start = (0, ypos)
            line_end = (self.size[0], ypos)
            ImageDraw.Draw(self.__image__).line([ line_start, line_end ], fill=colors["fg"], width=line_thickness)

    def __get_hour_sub_text__ (self, hour):
        if language is "de":
            return "Uhr"
        elif language is "en":
            return "AM" if hour < 12 else "PM"

    def __draw_event__ (self, event, column = 0):
        xoffset = hourbox_y_width * self.__row_size__[1]
        column_width = (self.size[0] - xoffset) / self.number_columns

        begin = event.begin_datetime
        time_ypos = self.__get_ypos_for_time__(begin.hour, begin.minute)
        hours = event.duration.total_seconds() / 3600
        time_height = self.__get_height_for_duration__(hours)

        pos = (xoffset + column_width * column, time_ypos)
        size = (column_width, time_height)

        self.__draw_event_block__(pos, size, event)

    def __draw_event_block__ (self, pos, size, event):
        box_color = colors["hl"] if event.highlight else colors["fg"]
        box = BoxDesign(size, fill = box_color)
        box.mask = False
        box.pos = pos
        self.draw_design(box)

        text = event.title
        text_color = colors["bg"]
        textbox_size = (size[0] - event_title_padding, size[1] - event_title_padding)
        txt = TextDesign(textbox_size, text = text, fontsize=event_title_fontsize, color=text_color, background_color=box_color)
        txt.pos = (pos[0] + event_title_padding, pos[1] + event_title_padding)
        self.draw_design(txt)