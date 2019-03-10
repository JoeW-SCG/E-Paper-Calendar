from DesignEntity import DesignEntity
from TableTextDesign import TableTextDesign

class EventListDesign (DesignEntity):
    """Creates a TableTextDesign filled with event
    begin date and title"""
    def __init__ (self, size, calendar, text_size = 16, filter_date=None, line_spacing=2, col_spacing=10, event_prefix_func=None):
        super(EventListDesign, self).__init__(size)
        self.calendar = calendar
        self.__event_matrix__ = []
        self.text_size = text_size
        self.filter_date = filter_date
        self.line_spacing = line_spacing
        self.col_spacing = col_spacing
        self.event_prefix_func = event_prefix_func
        if self.event_prefix_func is None:
            self.event_prefix_func = lambda x : self.__remove_leading_zero__(x.begin_datetime.strftime('%d %b'))

    def __finish_image__ (self):
        self.__fill_event_matrix__()
        
        col_hori_alignment = ['right', 'left']

        table_design = TableTextDesign(self.size, line_spacing=self.line_spacing, col_spacing=self.col_spacing, text_matrix=self.__event_matrix__, fontsize = self.text_size, column_horizontal_alignments=col_hori_alignment, mask=False, truncate_cols=False)
        self.draw_design(table_design)
    
    def __get_formatted_event__ (self, event):
        prefix = self.event_prefix_func(event)
        return [ prefix, event.title ]

    def __remove_leading_zero__(self, text):
        while text[0] is '0':
            text = text[1:]
        return text
    
    def __fill_event_matrix__ (self):
        for event in self.__get_events__():
            row = self.__get_formatted_event__(event)
            self.__event_matrix__.append(row)

    def __get_events__(self):
        upcoming = self.calendar.get_upcoming_events()
        if self.filter_date is not None:
            upcoming = [event for event in upcoming if event.begin_datetime.date() == self.filter_date]
        return upcoming