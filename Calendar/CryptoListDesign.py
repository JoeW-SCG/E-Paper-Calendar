from DesignEntity import DesignEntity
from TableDesign import TableDesign
from Assets import defaultfontsize
from GeckoCrypto import GeckoCrypto
from settings import crypto_coins


class CryptoListDesign (DesignEntity):
    def __init__ (self, size, crypto, text_size = defaultfontsize):
        super(CryptoListDesign, self).__init__(size)
        self.crypto = crypto
        self.text_size = text_size

    def __finish_image__ (self):
        matrix = self.__get_matrix__()
        col_spacing = 10
        if len(matrix) > 0:
            col_spacing = (self.size[0] / len(matrix[0])) * 0.5
        
        table_design = TableDesign(self.size, matrix=matrix, col_spacing=col_spacing, fontsize = self.text_size, mask=False, truncate_rows=True)
        self.draw_design(table_design)

    def __get_matrix__ (self):
        matrix = []
        coins = self.crypto.get_coins()
        for coin in coins:
            row = [ coin.symbol.upper(), coin.name, coin.currency + " " + str(coin.price), "% " + str(coin.day_change) ]
            matrix.append(row)
        return matrix
