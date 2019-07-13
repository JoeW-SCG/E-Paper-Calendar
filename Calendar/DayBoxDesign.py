from DesignEntity import DesignEntity
from SingelDayEventListDesign import SingelDayEventListDesign
from TextDesign import TextDesign

header_height = 0.2


class DayBoxDesign (DesignEntity):
    """Represents a day with its events in a box."""

    def __init__(self, size, date):
        super(DayBoxDesign, self).__init__(size)
        self.date = date

    def add_calendar(self, calendar):
        self.calendar = calendar

    def __finish_image__(self):
        self.__draw_header__()
        self.__draw_events__()

    def __draw_header__(self):
        pass

    def __draw_events__(self):
        events = self.calendar.get_day_events(self.date)

        pos = (0, self.size[1] * header_height)
        size = (self.size[0], self.size[1] - pos[1])

        event_list = SingelDayEventListDesign(size, events)
        event_list.pos = pos
        self.draw_design(event_list)
