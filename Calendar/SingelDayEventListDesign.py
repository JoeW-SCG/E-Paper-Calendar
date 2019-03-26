from EventListDesign import EventListDesign
from settings import hours
from Assets import fonts, defaultfontsize
from TextFormatter import event_time_summary

font = fonts["regular"]

class SingelDayEventListDesign (EventListDesign):
    """Specialized event list for day list design."""
    def __init__ (self, size, events, font_size = defaultfontsize, line_spacing=2, col_spacing=5, general_color="black", background_color="white", highlight_color="red"):
        prefix_func = lambda x : self.__get_event_prefix__(x)
        super().__init__(size, events, text_size=font_size, line_spacing=line_spacing, col_spacing=col_spacing, event_prefix_func=event_time_summary, font_family=font, show_more_info=True, general_color=general_color, background_color=background_color, highlight_color = highlight_color)