from DesignEntity import DesignEntity

class HourListDesign (DesignEntity):
    """Hours of a day are listed vertically and
    resemble a timeline."""
    def __init__ (self, size, first_hour):
        super(HourListDesign, self).__init__(size)

    def add_events(self, events):
        pass