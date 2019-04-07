from EventListDesign import EventListDesign
from settings import hours
from Assets import fonts, defaultfontsize, colors
from TextFormatter import event_prefix_str_sum

font = fonts["regular"]

class SingelDayEventListDesign (EventListDesign):
    """Specialized event list for day list design."""
    def __init__ (self, size, events, font_size = defaultfontsize, line_spacing=2, event_prefix_rel_dates = [], col_spacing=5, general_color=colors["fg"], background_color=colors["bg"], highlight_color=colors["hl"]):
        prefix_func = lambda x, rel_date : event_prefix_str_sum(x, rel_date)
        super().__init__(size, events, text_size=font_size, line_spacing=line_spacing, col_spacing=col_spacing, event_prefix_rel_dates = event_prefix_rel_dates, event_prefix_func=prefix_func, font_family=font, show_more_info=True, general_color=general_color, background_color=background_color, highlight_color = highlight_color)