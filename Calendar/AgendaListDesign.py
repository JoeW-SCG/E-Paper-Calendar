from DesignEntity import DesignEntity
from Assets import defaultfontsize
from datetime import datetime, date, timedelta
from SingelDayEventListDesign import SingelDayEventListDesign

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
        #self.__draw_dates__()
        #self.__draw_lines__()

    def __calculate_parameter__ (self):
        self.__line_height__ = self.line_spacing + int(self.text_size)
        self.__event_number__ = int(int(self.size[1]) // self.__line_height__)
        self.__date_fontsize__ = self.__line_height__
        self.__date_width__ = 50

    def __fetch_events__ (self):
        self.__events__ = []
        fetch_day = self.start_dt
        while len(self.__events__) < self.__event_number__:
            self.__events__.extend(self.calendar.get_day_events(fetch_day))
            fetch_day = fetch_day + timedelta(1)
            
    def __draw_events__ (self):
        size = (self.size[0] - self.__date_width__, self.size[1])

        events = SingelDayEventListDesign(size, self.__events__, font_size=self.text_size, line_spacing=self.line_spacing)
        events.pos = (self.__date_width__, 0)
        self.draw_design(events)

    def __draw_dates__ (self):
        raise NotImplementedError()

    def __draw_lines__ (self):
        raise NotImplementedError()