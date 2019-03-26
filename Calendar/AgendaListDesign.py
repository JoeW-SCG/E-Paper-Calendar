from DesignEntity import DesignEntity
from Assets import defaultfontsize
from datetime import datetime, date, timedelta
from SingelDayEventListDesign import SingelDayEventListDesign
from TableTextDesign import TableTextDesign
from PIL import ImageDraw

line_color = "black"
line_width = 1

class AgendaListDesign (DesignEntity):
    '''Lists upcoming events in chronological order and groups them by days'''
    def __init__ (self, size, calendar, line_spacing = 3, text_size = defaultfontsize, start_date = date.today()):
        super(AgendaListDesign, self).__init__(size)
        self.calendar = calendar
        self.line_spacing = line_spacing
        self.text_size = text_size
        self.start_dt = datetime(start_date.year, start_date.month, start_date.day)

    def __finish_image__ (self):
        self.__calculate_parameter__()
        self.__fetch_events__()
        self.__draw_events__()
        self.__draw_dates__()
        self.__draw_lines__()

    def __calculate_parameter__ (self):
        self.__line_height__ = self.line_spacing + int(self.text_size)
        self.__event_number__ = int(int(self.size[1]) // self.__line_height__)
        self.__date_fontsize__ = self.text_size
        self.__date_width__ = self.__date_fontsize__ * 5
        self.__date_linespace__ = self.line_spacing

    def __fetch_events__ (self):
        self.__events__ = []
        self.__dates__ = []
        fetch_day = self.start_dt
        while len(self.__events__) < self.__event_number__:
            day_events = self.calendar.get_day_events(fetch_day)
            self.__events__.extend(day_events)
            for _ in range(len(day_events)):
                self.__dates__.append(fetch_day)
            fetch_day = fetch_day + timedelta(1)
            
    def __draw_events__ (self):
        size = (self.size[0] - self.__date_width__, self.size[1])

        events = SingelDayEventListDesign(size, self.__events__, font_size=self.text_size, line_spacing=self.line_spacing)
        events.pos = (self.__date_width__, 0)
        self.draw_design(events)

    def __draw_dates__ (self):
        size = (self.__date_width__, self.size[1])

        date_matrix = self.__get_date_matrix__()
        table = TableTextDesign(size, date_matrix, fontsize = self.__date_fontsize__, line_spacing=self.__date_linespace__)
        table.pos = (0, 0)
        self.draw_design(table)

    def __get_date_matrix__ (self):
        matrix = []
        last_date = ""
        for date in self.__dates__:
            current_date = date.strftime(" %d. %b")
            if current_date != last_date:
                last_date = current_date
                matrix.append([current_date])
            else:
                matrix.append([""])
        return matrix

    def __draw_lines__ (self):
        for i, (first, second) in enumerate(zip(self.__dates__, self.__dates__[1:])):
            if first is not second:
                self.__draw_line__(i + 1)

    def __draw_line__(self, index):
        ypos = index * self.__line_height__ - self.line_spacing / 2
        pos = (0, ypos)
        positions = [pos, (self.size[0], ypos)]

        ImageDraw.Draw(self.__image__).line(positions, fill=line_color, width=line_width)