class DisplayAdapter (object):
    """Interface for CalendarDesign output channels."""
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render (self, design):
        raise NotImplementedError("Functions needs to be implemented")

    def calibrate (self):
        raise NotImplementedError("Functions needs to be implemented")