class CalendarEvent (object):
    """Defines a calendar event, independent of any implementation"""

    def __init__(self):
        self.begin_datetime = None
        self.end_datetime = None
        self.duration = None
        self.allday = None
        self.multiday = None
        self.rrule = None

        self.title = None
        self.description = None
        self.attendees = []
        self.highlight = None

        self.calendar_name = None

        self.location = None
        self.fetch_datetime = None

    def __repr__(self):
        return self.title
