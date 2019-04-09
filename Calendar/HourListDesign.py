from DesignEntity import DesignEntity
from settings import hours, language
from TextDesign import TextDesign
from PIL import ImageDraw
from Assets import colors, defaultfontsize
from BoxDesign import BoxDesign
from datetime import timedelta, datetime

hourbox_y_width = 1
hour_box_fontsize = 0.8
hoursubtext_fontsize = 0.8
hoursubtext_height = 0.38
event_title_fontsize = defaultfontsize
event_title_padding = 3
line_thickness = 1
currenttimeline_thickness = 1

class HourListDesign (DesignEntity):
    """Hours of a day are listed vertically and
    resemble a timeline."""
    def __init__ (self, size, first_hour = 0, last_hour = 23):
        super(HourListDesign, self).__init__(size)
        self.first_hour = first_hour
        self.last_hour = last_hour
        self.__calc_parameters__()
        self.events = []

    def add_events (self, events):
        self.events.extend(events)

    def __finish_image__ (self):
        self.number_columns = self.__get_max_num_simultaneous_events__()
        self.__draw_hour_rows__()
        self.__draw_lines__()
        self.__draw_events__()
        self.__draw_current_time_line__()

    def __calc_parameters__ (self):
        self.hour_count = self.last_hour - self.first_hour
        self.row_size = (self.size[0], self.size[1] / self.hour_count)

    def __get_hour_text__ (self, hour):
        if hour <= 12 or hours is "24":
            return str(hour)
        else:
            short = hour - 12
            return str(short) if short > 0 else "12"

    def __get_ypos_for_time__ (self, hour, minute = 0):
        return self.__get_height_for_duration__(hour, minute) - self.__get_height_for_duration__(self.first_hour)

    def __get_height_for_duration__ (self, hours, minutes = 0):
        row_height = self.row_size[1]
        return row_height * (hours + minutes / 60)

    def __draw_events__ (self):
        column_events = []
        for _ in range(self.number_columns):
            column_events.append(None)
        for event in self.events:
            column_events = self.__update_columns_events__(column_events, event)
            self.__draw_event__(event, column_events.index(event))

    def __update_columns_events__ (self, column_events, new_event):
        current_time = new_event.begin_datetime
        new_event_added = False
        for index in range(len(column_events)):
            if column_events[index] != None and column_events[index].end_datetime <= current_time:
                column_events[index] = None
            if new_event_added == False and column_events[index] == None:
                column_events[index] = new_event
                new_event_added = True
        return column_events

    def __draw_hour_rows__ (self):
        for hour in range(self.first_hour, self.last_hour + 1):
            self.__draw_row__(hour)

    def __draw_row__ (self, hour):
        subtext_height = self.row_size[1] * hoursubtext_height
        sub_fontsize = subtext_height * hoursubtext_fontsize
        width = hourbox_y_width * self.row_size[1]
        height = self.row_size[1] - subtext_height
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
            ypos = i * self.row_size[1]
            line_start = (0, ypos)
            line_end = (self.size[0], ypos)
            ImageDraw.Draw(self.__image__).line([ line_start, line_end ], fill=colors["fg"], width=line_thickness)

    def __get_hour_sub_text__ (self, hour):
        if hours == "12":
            return "AM" if hour < 12 else "PM"
        elif language is "de":
            return "Uhr"
        elif language is "en":
            return "o'c"

    def __draw_event__ (self, event, column = 0):
        xoffset = hourbox_y_width * self.row_size[1]
        column_width = (self.size[0] - xoffset) / self.number_columns

        begin = event.begin_datetime
        time_ypos = self.__get_ypos_for_time__(begin.hour, begin.minute)
        hours = event.duration.total_seconds() / 3600
        time_height = self.__get_height_for_duration__(hours)

        yoffset_correction = 0
        if time_ypos < 0:
            yoffset_correction = time_ypos

        pos = (xoffset + column_width * column, time_ypos - yoffset_correction)
        size = (column_width, time_height + yoffset_correction)

        if size[1] < 0:
            return  #Event not in shown time range

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
        txt = TextDesign(textbox_size, text = text, fontsize=event_title_fontsize, color=text_color, background_color=box_color, wrap=True)
        txt.mask = False
        txt.pos = (pos[0] + event_title_padding, pos[1] + event_title_padding)
        self.draw_design(txt)

    def __get_max_num_simultaneous_events__ (self):
        parallelity_count = 1

        for index, event in enumerate(self.events):
            current_parallelity = 1
            preceding = self.events[:index] #Assumption: Events are ordered chronologically
            for pre_event in preceding:
                if self.__are_simultaneous__(event, pre_event):
                    current_parallelity += 1
            if parallelity_count < current_parallelity:
                parallelity_count = current_parallelity
        return parallelity_count

    def __are_simultaneous__ (self, ev_a, ev_b):
        if ev_a.begin_datetime > ev_b.begin_datetime:
            ev_a, ev_b = ev_b, ev_a
        
        mes_dur = ev_b.begin_datetime - ev_a.begin_datetime

        return mes_dur < ev_a.duration

    def __draw_current_time_line__(self):
        now = datetime.now()
        ypos = self.__get_ypos_for_time__(now.hour, now.minute)
        
        line_start = (0, ypos)
        line_end = (self.size[0], ypos)
        ImageDraw.Draw(self.__image__).line([ line_start, line_end ], fill=colors["hl"], width=currenttimeline_thickness)