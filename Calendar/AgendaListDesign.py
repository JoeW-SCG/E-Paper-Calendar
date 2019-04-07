from DesignEntity import DesignEntity
from Assets import defaultfontsize, colors
from datetime import datetime, date, timedelta
from TableTextDesign import TableTextDesign
from PIL import ImageDraw
from TextFormatter import date_summary_str, event_prefix_str

line_width = 1

class AgendaListDesign (DesignEntity):
    '''Lists upcoming events in chronological order and groups them by days'''
    def __init__ (self, size, calendar, line_spacing = 3, col_spacing = 6, text_size = defaultfontsize, start_date = date.today()):
        super(AgendaListDesign, self).__init__(size)
        self.calendar = calendar
        self.line_spacing = line_spacing
        self.col_spacing = col_spacing
        self.text_size = text_size
        self.start_dt = datetime(start_date.year, start_date.month, start_date.day)

    def __finish_image__ (self):
        self.__calculate_parameter__()
        self.__create_infos_events__()
        self.__draw_infos__()
        self.__draw_lines__()

    def __calculate_parameter__ (self):
        self.__line_height__ = self.line_spacing + int(self.text_size)
        self.__event_number__ = int(int(self.size[1]) // self.__line_height__)
        self.__date_fontsize__ = self.text_size
        self.__date_linespace__ = self.line_spacing

    def __create_infos_events__ (self):
        self.infos = []
        self.cell_props = []
        last_date = ""
        fetch_day = self.start_dt
        while len(self.infos) < self.__event_number__:
            day_events = self.calendar.get_day_events(fetch_day)
            fetch_day_added_once = False
            for event in day_events:
                row = [ "" ]
                if fetch_day_added_once is False:
                    row.append(date_summary_str(fetch_day))
                    fetch_day_added_once = True
                else:
                    row.append("")

                row.append(event_prefix_str(event, fetch_day))
                row.append(event.title)
                self.cell_props.append(self.__get_row_props__(event))
                
                self.infos.append(row)
            fetch_day = fetch_day + timedelta(1)
            
    def __draw_infos__ (self):
        table = TableTextDesign(self.size, self.infos, fontsize = self.__date_fontsize__, line_spacing=self.__date_linespace__, col_spacing = self.col_spacing, cell_properties=self.cell_props)
        self.draw_design(table)

    def __draw_lines__ (self):
        for i, (_, date, _, _) in enumerate(self.infos[1:]):
            if date is not "":
                self.__draw_line__(i + 1)

    def __draw_line__ (self, index):
        ypos = index * self.__line_height__ - self.line_spacing / 2
        pos = (0, ypos)
        positions = [ pos, (self.size[0], ypos) ]

        ImageDraw.Draw(self.__image__).line(positions, fill=colors["fg"], width=line_width)

    def __get_row_props__ (self, event = None):
        color = colors["fg"]
        bg_color = colors["bg"]
        default_cell = {
            "color" : color,
            "background_color" : bg_color
        }
        if event is not None and event.highlight:
            color = colors["hl"]
        cell = {
            "color" : color,
            "background_color" : bg_color
        }
        return [default_cell, default_cell, cell, cell ]