from DesignEntity import DesignEntity
from PIL import ImageFont, ImageDraw, ImageOps
from Assets import path, defaultfont

paddingcorrection = -5

class TextDesign (DesignEntity):
    """Object that manages all information relevant to text
    and prints it to an image"""
    def __init__ (self, size, font = None, fontsize = 12, text = "", horizontalalignment = "left", verticalalignment = "top", mask=True):
        super(TextDesign, self).__init__(size, mask = mask)
        if font is None:
            font = defaultfont
        self.font_family = font
        self.font_size = fontsize
        self.text = text
        self.horizontal_alignment = horizontalalignment
        self.vertical_alignment = verticalalignment

    def __finish_image__ (self):
        self.__init_image__()
        self.__font__ = self.__get_font__()
        pos = self.__pos_from_alignment__()
        ImageDraw.Draw(self.__image__).text(pos, self.text, fill=0, font=self.__font__)

    def __pos_from_alignment__ (self):
        width, height = self.__font__.getsize(self.text)
        x, y = 0, 0
        
        if self.vertical_alignment == "center":
            y = int((self.size[1] / 2) - (height / 2))
        elif self.vertical_alignment == "bottom":
            y = int(self.size[1] - height)

        if self.horizontal_alignment == "center":
            x = int((self.size[0] / 2) - (width / 2))
        elif self.vertical_alignment == "right":
            x = int(self.size[0] - width)

        return (x, y + paddingcorrection)

    def __get_font__(self):
        return ImageFont.truetype(path + self.font_family, self.font_size)