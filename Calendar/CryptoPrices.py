from CryptoInterface import CryptoInterface
from datetime import datetime, timedelta, date
import CryptoItem
import urllib.request
import json
import math


class CryptoPrices(CryptoInterface):
    def __init__(self, coins):
        self.coins = coins
        super(CryptoPrices, self).__init__()

    def is_available(self):
        if len(self.coins) > 0 and len(self.coins) < 8:
            return True
        else:
            return False

    def __get_prices__(self):
        price=[]
        name=[]
        for coin in self.coins:
            data = urllib.request.urlopen("https://api.coingecko.com/api/v3/simple/price?ids="+coin+"&vs_currencies=USD").read()
            dataJSON = json.loads(data.decode('utf-8'))
            raw = dataJSON[coin]["usd"]
            price.append(math.ceil(raw*100)/100)
            name.append(coin)
        return price,name
