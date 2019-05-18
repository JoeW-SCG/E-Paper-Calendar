class CryptoCoin(object):
    def __init__ (self):
        self.name = None
        self.symbol = None
        self.price = None
        self.day_change = None
        self.currency = None
        self.datetime = None

        self.fetch_datetime = None