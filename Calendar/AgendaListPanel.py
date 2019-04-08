from PanelDesign import PanelDesign
from AgendaListDesign import AgendaListDesign
from WeatherHeaderDesign import WeatherHeaderDesign
from settings import general_settings
from PIL import ImageDraw
from Assets import colors
from RssPostListDesign import RssPostListDesign

agenda_ypadding = 5
weatherheader_height = 0.113
seperator_width = 3
infolist_size = (1, 0.24)
infolist_padding = 5

class AgendaListPanel (PanelDesign):
    '''Lists upcoming events in chronological order and groups them by days'''
    def __init__(self, size):
        super(AgendaListPanel, self).__init__(size)
        self.weather_size = (0, 0)
        self.info_size = (0, 0)
        if general_settings["weather-info"]:
            self.weather_size = (self.size[0], self.size[1] * weatherheader_height)

    def add_weather (self, weather):
        self.weather = weather

    def add_calendar (self, calendar):
        self.calendar = calendar

    def add_rssfeed (self, rss):
        if general_settings["info-area"] != "rss":
            return

        self.info_size = self.__abs_pos__(infolist_size)
        pos = (0, self.size[1] - self.info_size[1] + infolist_padding)

        list = RssPostListDesign(self.info_size, rss)
        list.pos = pos
        self.draw_design(list)

        self.__draw_seperator__(1-infolist_size[1], colors["fg"])

    def add_taks (self, tasks):
        pass

    def __finish_panel__(self):
        self.__draw_calendar__()
        if general_settings["weather-info"]:
            self.__draw_weather__()

    def __draw_seperator__ (self, height, color):
        ImageDraw.Draw(self.__image__).line([ self.__abs_pos__((0, height)), self.__abs_pos__((1, height)) ], fill=color, width=seperator_width)

    def __abs_pos__ (self, pos, size = None):
        if size is None:
            size = self.size
        return (int(pos[0] * size[0]), int(pos[1] * size[1]))

    def __draw_calendar__(self):
        size = (self.size[0], self.size[1] - self.weather_size[1] - self.info_size[1] - agenda_ypadding)

        agenda = AgendaListDesign(size, self.calendar)
        agenda.pos = (0, agenda_ypadding + self.weather_size[1])
        self.draw_design(agenda)

    def __draw_weather__(self):
        header = WeatherHeaderDesign(self.weather_size, self.weather)
        self.draw_design(header)
        self.__draw_seperator__(weatherheader_height, colors["hl"])