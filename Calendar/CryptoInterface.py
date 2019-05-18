from DataSourceInterface import DataSourceInterface

class CryptoInterface(DataSourceInterface):
    def __init__(self):
        self.crypto_coins = []

    def reload(self):
        if self.is_available() == False:
            return
        self.crypto_coins = self.__get_coins__()

    def __get_coins__(self):
        raise NotImplementedError("Function needs to be implemented")

    def get_coins(self):
        return self.crypto_coins
