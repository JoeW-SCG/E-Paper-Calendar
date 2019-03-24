from PanelDesign import PanelDesign
from AgendaListDesign import AgendaListDesign

agenda_ypadding = 5

class AgendaListPanel (PanelDesign):
    '''Lists upcoming events in chronological order and groups them by days'''
    def __init__(self, size):
        super(AgendaListPanel, self).__init__(size)

    def add_weather (self, weather):
        pass

    def add_calendar (self, calendar):
        agenda = AgendaListDesign(self.size, calendar)
        agenda.pos = (0, agenda_ypadding)
        self.draw_design(agenda)

    def add_rssfeed (self, rss):
        pass

    def add_taks (self, tasks):
        pass