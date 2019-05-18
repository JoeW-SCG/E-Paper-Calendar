from DataSourceInterface import DataSourceInterface
from datetime import datetime, timezone, timedelta

class CryptoInterface(DataSourceInterface):
    def __init__(self):
        self.crypto_prices = []

    def reload(self):
        if self.is_available() == False:
            return
        self.crypto_prices= self.__get_prices__()
        self.sort_prices()

    def __get_prices__(self):
        raise NotImplementedError("Functions needs to be implemented")

    def get_latest_prices(self):
        self.crypto_prices = self.crypto_prices
        return self.crypto_prices

    def sort_prices(self):
        self.crypto_prices =self.crypto_prices
