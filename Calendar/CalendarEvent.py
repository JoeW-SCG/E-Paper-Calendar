class CalendarEvent (object):
    """Defines a calendar event, independent of any implementation"""
    def __init__ (self):
        self.date = None
        self.time = None
        self.duration = None

        self.title = None
        self.description = None
        self.attendees = []
        self.highlight = None

        self.place = None
        self.fetch_time = None