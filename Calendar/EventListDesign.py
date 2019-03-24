from DesignEntity import DesignEntity
from TableTextDesign import TableTextDesign
from settings import language

class EventListDesign (DesignEntity):
    """Creates a TableTextDesign filled with event
    begin date and title"""
    def __init__ (self, size, events, text_size = 16, line_spacing = 2, col_spacing = 10, event_prefix_func = None, font_family = None, general_color = "black", background_color = "white", highlight_color = "red", show_more_info = False):
        super(EventListDesign, self).__init__(size)
        self.events = events
        self.__event_matrix__ = []
        self.__props_matrix__ = []
        self.show_more_info = show_more_info
        self.text_size = text_size
        self.line_spacing = line_spacing
        self.col_spacing = col_spacing
        self.font_family = font_family
        self.general_color = general_color
        self.background_color = background_color
        self.highlight_color = highlight_color
        self.event_prefix_func = event_prefix_func
        if self.event_prefix_func is None:
            self.event_prefix_func = lambda x : self.__remove_leading_zero__(x.begin_datetime.strftime('%d %b'))

    def __finish_image__ (self):
        self.visible_event_count = int((self.size[1] - self.line_spacing) // (self.line_spacing + self.text_size))
        self.__fill_event_matrix__()
        
        col_hori_alignment = [ 'right', 'left' ]
        table_design = TableTextDesign(self.size, background_color = self.background_color, font=self.font_family, line_spacing=self.line_spacing, col_spacing=self.col_spacing, text_matrix=self.__event_matrix__, fontsize = self.text_size, column_horizontal_alignments=col_hori_alignment, mask=False, truncate_cols=False, cell_properties=self.__props_matrix__)
        self.draw_design(table_design)
    
    def __get_formatted_event__ (self, event):
        prefix = self.event_prefix_func(event)
        return [ prefix, event.title ]

    def __remove_leading_zero__ (self, text):
        while text[0] is '0':
            text = text[1:]
        return text
    
    def __fill_event_matrix__ (self):
        visible_events = self.events
        if self.show_more_info and len(visible_events) > self.visible_event_count:
            visible_events = visible_events[:self.visible_event_count - 1]
        for event in visible_events:
            row = self.__get_formatted_event__(event)
            self.__event_matrix__.append(row)
            self.__props_matrix__.append(self.__get_row_props__(event))

        if self.show_more_info is False:
            return

        additional_events_count = len(self.events) - len(visible_events)
        more_text = self.__get_more_text__()
        if additional_events_count > 0:
            self.__event_matrix__.append([ "", " + " + str(additional_events_count) + " " + more_text ])
            self.__props_matrix__.append(self.__get_row_props__(event))

    def __get_row_props__ (self, event = None):
        color = self.general_color
        bg_color = self.background_color
        if event is not None and event.highlight:
            color = self.highlight_color
        cell = {
            "color" : color,
            "background_color" : bg_color
        }
        return [ cell, cell ]

    def __get_more_text__ (self):
        more_texts = {
            "de" : "weitere",
            "en" : "more"
            }
        return more_texts[language]