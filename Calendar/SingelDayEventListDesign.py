from EventListDesign import EventListDesign
from settings import hours
from Assets import fonts

eventlist_allday_char = "•"
font = fonts["regular"]

class SingelDayEventListDesign (EventListDesign):
    """Specialized event list for day list design."""
    def __init__ (self, size, events, font_size = 16, line_spacing=2, col_spacing=5, general_color="black", background_color="white", highlight_color="red"):
        prefix_func = lambda x : self.__get_event_prefix__(x)
        super().__init__(size, events, text_size=font_size, line_spacing=line_spacing, col_spacing=col_spacing, event_prefix_func=prefix_func, font_family=font, show_more_info=True, general_color=general_color, background_color=background_color, highlight_color = highlight_color)
    
    def __get_event_prefix__ (self, event):
        if event.allday:
            return eventlist_allday_char
        else:
            return self.__get_time__(event.begin_datetime)

    def __get_time__ (self, time):
        if hours == "24":
            return time.strftime('%H:%M')
        else:
            return time.strftime('%I:%M')