from CryptoInterface import CryptoInterface
from datetime import datetime
from CryptoCoin import CryptoCoin
from urllib.request import urlopen
import json
import math

api_test_url = "https://api.coingecko.com/api/v3/ping"
api_url = "https://api.coingecko.com/api/v3/"
api_metadata_url = api_url + "coins/list"
api_price_url = api_url + "simple/price"
price_currency = "usd"
price_currency_sign = "$"


class GeckoCrypto(CryptoInterface):
    def __init__(self, coins):
        self.coin_ids = coins
        self.metadata = None
        super(GeckoCrypto, self).__init__()

    def is_available(self):
        try:
            urlopen(api_test_url)
            return True
        except:
            return False

    def __get_coins__(self):
        if len(self.coin_ids) == 0:
            return []

        self.__prepare_metadata__()
        coins = []
        for id in self.coin_ids:
            try:
                data = urlopen(api_price_url + "?include_24hr_change=true&ids=" +
                               self.metadata[id]['id'] + "&vs_currencies=" + price_currency).read()
                dataJSON = json.loads(data.decode('utf-8'))
                raw = dataJSON[id][price_currency]
                price = math.ceil(raw*100) / 100
                change = dataJSON[id]['usd_24h_change']

                coins.append(self.__build_coin__(id, price, change))
            except:
                print("Gecko-Error [" + id + "]")
        return coins

    def __build_coin__(self, id, value, change):
        coin = CryptoCoin()

        coin.name = self.metadata[id]['name']
        coin.day_change = round(change, 2)
        coin.price = value

        coin.datetime = datetime.now()
        coin.fetch_datetime = datetime.now()
        coin.currency = price_currency_sign
        coin.symbol = self.metadata[id]['symbol']

        return coin

    def __prepare_metadata__(self):
        self.metadata = None
        data = urlopen(api_metadata_url).read()
        dataJSON = json.loads(data.decode('utf-8'))
        self.metadata = {coin['id'].lower(
        ): coin for coin in dataJSON if coin['id'].lower() in self.coin_ids}
