from DesignEntity import DesignEntity
from TableTextDesign import TableTextDesign

col_sizes = [0.15, 0.85]

class EventListDesign (DesignEntity):
    """Creates a TableTextDesign filled with event
    begin date and title"""
    def __init__ (self, size, calendar, event_count = None, text_size = 16):
        super(EventListDesign, self).__init__(size)
        self.calendar = calendar
        self.__event_matrix__ = []
        self.text_size = text_size

    def __finish_image__ (self):
        self.__fill_event_matrix__()
        
        max_col_size = [int(col_sizes[0] * self.size[0]), int(col_sizes[1] * self.size[0])]

        table_design = TableTextDesign(self.size, line_spacing=3, col_spacing=5, text_matrix=self.__event_matrix__, fontsize = self.text_size, mask=False, max_col_size = max_col_size, truncate_cols=False)
        self.draw_design(table_design)
    
    def __get_formatted_event__ (self, event):
        return [ event.begin_datetime.strftime('%d %b'), event.title ]
    
    def __fill_event_matrix__ (self):
        for event in self.calendar.get_upcoming_events():
            row = self.__get_formatted_event__(event)
            self.__event_matrix__.append(row)