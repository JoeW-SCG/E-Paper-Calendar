from EventListDesign import EventListDesign
from settings import hours

eventlist_colspacing = 5
eventlist_allday_char = "•"

class SingelDayEventListDesign (EventListDesign):
    """Specialized event list for day list design."""
    def __init__ (self, size, calendar, date, font_size = 16):
        prefix_func = lambda x : self.__get_event_prefix__(x)
        super().__init__(size, calendar, filter_date=date, text_size=font_size, event_prefix_func=prefix_func, col_spacing=eventlist_colspacing)
    
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