class RssPost(object):
    """Defines a rss post, independent of any implementation"""

    def __init__(self):
        self.title = None
        self.description = None
        self.source = None

        self.datetime = None
        self.fetch_datetime = None
