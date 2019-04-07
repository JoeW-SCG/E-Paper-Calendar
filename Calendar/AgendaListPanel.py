from PanelDesign import PanelDesign
from AgendaListDesign import AgendaListDesign
from WeatherHeaderDesign import WeatherHeaderDesign
from settings import general_settings
from PIL import ImageDraw
from Assets import colors

agenda_ypadding = 5
weatherheader_height = 0.113
seperatorplace = (0, 0.113)
seperator_width = 1

class AgendaListPanel (PanelDesign):
    '''Lists upcoming events in chronological order and groups them by days'''
    def __init__(self, size):
        super(AgendaListPanel, self).__init__(size)
        self.weather_size = (0, 0)
        if general_settings["weather-info"]:
            self.weather_size = (self.size[0], self.size[1] * weatherheader_height)

    def add_weather (self, weather):
        self.weather = weather

    def add_calendar (self, calendar):
        size = (self.size[0], self.size[1] - self.weather_size[1])

        agenda = AgendaListDesign(size, calendar)
        agenda.pos = (0, agenda_ypadding + self.weather_size[1])
        self.draw_design(agenda)

    def add_rssfeed (self, rss):
        pass

    def add_taks (self, tasks):
        pass

    def __finish_image__(self):
        if general_settings["weather-info"] == False:
            return
        header = WeatherHeaderDesign(self.weather_size, self.weather)
        self.draw_design(header)
        self.__draw_seperator__()

    def __draw_seperator__ (self):
        """Draw a line seperating the weather and Calendar section"""
        ImageDraw.Draw(self.__image__).line([ self.__abs_pos__(seperatorplace), self.__abs_pos__((1, seperatorplace[1])) ], fill=colors["hl"], width=seperator_width)

    def __abs_pos__ (self, pos, size = None):
        if size is None:
            size = self.size
        return (int(pos[0] * size[0]), int(pos[1] * size[1]))