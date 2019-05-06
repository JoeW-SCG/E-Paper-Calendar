from DesignEntity import DesignEntity
from TableDesign import TableDesign
from Assets import defaultfontsize, colors
from TextFormatter import date_str
from DictionaryMapper import get_text
from Dictionary import more_events

class EventListDesign (DesignEntity):
    """Creates a TableDesign filled with event
    begin date and title"""
    def __init__ (self, size, events, text_size = defaultfontsize, line_spacing = 2, col_spacing = 10, event_prefix_rel_dates = [], event_prefix_func = None, font_family = None, general_color = colors["fg"], background_color = colors["bg"], highlight_color = colors["hl"], show_more_info = False):
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
        self.event_prefix_rel_dates = event_prefix_rel_dates
        if self.event_prefix_func is None:
            self.event_prefix_func = lambda x, y : date_str(x.begin_datetime)

    def __finish_image__ (self):
        self.visible_event_count = int(int(self.size[1] + self.line_spacing) // (self.line_spacing + int(self.text_size)))
        self.__fill_event_matrix__()
        
        col_hori_alignment = [ 'right', 'left' ]
        table_design = TableDesign(self.size, background_color = self.background_color, font=self.font_family, line_spacing=self.line_spacing, col_spacing=self.col_spacing, matrix=self.__event_matrix__, fontsize = self.text_size, column_horizontal_alignments=col_hori_alignment, mask=False, truncate_cols=False, cell_properties=self.__props_matrix__)
        self.draw_design(table_design)
    
    def __get_formatted_event__ (self, event, index):
        rel_date = None if index < 0 or index >= len(self.event_prefix_rel_dates) else self.event_prefix_rel_dates[index]
        prefix = self.event_prefix_func(event, rel_date)
        return [ prefix, event.title ]
    
    def __fill_event_matrix__ (self):
        visible_events = self.events
        if self.show_more_info and len(visible_events) > self.visible_event_count:
            visible_events = visible_events[:self.visible_event_count - 1]
        for i, event in enumerate(visible_events):
            row = self.__get_formatted_event__(event, i)
            self.__event_matrix__.append(row)
            self.__props_matrix__.append(self.__get_row_props__(event))

        if self.show_more_info is False:
            return

        additional_events_count = len(self.events) - len(visible_events)
        more_text = " " + get_text(more_events, additional_events_count)
        if additional_events_count > 0:
            self.__event_matrix__.append([ "", more_text ])
            self.__props_matrix__.append(self.__get_row_props__())

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