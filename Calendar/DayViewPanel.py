from PanelDesign import PanelDesign
from datetime import datetime, timedelta, date

class DayViewPanel (PanelDesign):
    """Overview that focuses on the current day and
    shows a timeline split into hours."""
    def __init__ (self, size):
        super(DayViewPanel, self).__init__(size)
        self.__first_render__()

    def __first_render__ (self):
        pass

    def add_weather (self, weather):
        pass

    def add_calendar (self, calendar):
        pass

    def add_rssfeed (self, rss):
        pass

    def add_taks (self, tasks):
        pass

    def __finish_image__(self):
        pass

    def __abs_co__(self, coordinates):
        return (int(coordinates[0] * self.size[0]),int(coordinates[1] * self.size[1]))