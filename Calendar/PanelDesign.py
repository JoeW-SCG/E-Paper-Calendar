class PanelDesign(object):
    """Defined general interface for panel designs."""
    def set_size(self, width, height):
        self.width = width
        self.height = height

    def get_image (self):
        raise NotImplementedError("Functions needs to be implemented")

    def add_weather (self, weather):
        raise NotImplementedError("Functions needs to be implemented")

    def add_calendar (self, calendar):
        raise NotImplementedError("Functions needs to be implemented")

    def add_rssfeed (self, rss):
        raise NotImplementedError("Functions needs to be implemented")