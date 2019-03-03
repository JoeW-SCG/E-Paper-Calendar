from DesignEntity import DesignEntity

class PanelDesign (DesignEntity):
    """Defined general interface for panel designs."""
    def __init__ (self, size):
        super(PanelDesign, self).__init__(size)

    def add_weather (self, weather):
        raise NotImplementedError("Functions needs to be implemented")

    def add_calendar (self, calendar):
        raise NotImplementedError("Functions needs to be implemented")

    def add_rssfeed (self, rss):
        raise NotImplementedError("Functions needs to be implemented")

    def add_taks (self, tasks):
        raise NotImplementedError("Functions needs to be implemented")