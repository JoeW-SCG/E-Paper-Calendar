from DesignEntity import DesignEntity

class WeatherColumnDesign(DesignEntity):
    """Displays weather information in a column"""
    def __init__(self, size):
        super().__init__(size)

    def __finish_image__(self):
        pass