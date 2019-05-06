from DesignEntity import DesignEntity

class DayBoxDesign (DesignEntity):
    """Represents a day with its events in a box."""
    def __init__(self, size, date):
        super(DayBoxDesign, self).__init__(size)
        self.date = date

    def add_calendar(self, calendar):
        pass

    def __finish_image__(self):
        pass