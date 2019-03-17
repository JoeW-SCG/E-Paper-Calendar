from DesignEntity import DesignEntity
from PIL import ImageFont, ImageDraw, ImageOps
from Assets import path, defaultfont
from TextWraper import wrap_text_with_font

paddingcorrection = -3
truncateerror_fontsize = 0.5

class TextDesign (DesignEntity):
    """Object that manages all information relevant to text
    and prints it to an image"""
    def __init__ (self, size, color="black", background_color="white", font = None, fontsize = 12, text = "", horizontalalignment = "left", verticalalignment = "top", mask=True, truncate=False, truncate_suffix = '...', wrap=False):
        super(TextDesign, self).__init__(size, mask = mask)
        if font is None:
            font = defaultfont
        self.font_family = font
        self.font_size = fontsize
        self.text = text
        self.horizontal_alignment = horizontalalignment
        self.vertical_alignment = verticalalignment
        self.truncate = truncate
        self.truncate_suffix = truncate_suffix
        self.wrap = wrap
        self.color = color
        self.background_color = background_color

    def __finish_image__ (self):
        if self.color is "white":
            self.invert_mask = True
        if self.background_color not in ["white", "black"]:
            self.color_key = True
        self.__init_image__(self.background_color)

        self.__font__ = self.__get_font__()
        if self.wrap is False and self.truncate:
            self.__truncate_text__()
        if self.wrap:
            self.__wrap_text__()
        pos = self.__pos_from_alignment__()
        ImageDraw.Draw(self.__image__).text(pos, self.text, fill=self.color, font=self.__font__)
        
    def __truncate_text__ (self):
        if self.__font__.getsize_multiline(self.text)[0] <= self.size[0]: #does not need truncating
            return
        error = truncateerror_fontsize * self.__font__.getsize_multiline("A")[0]
        suffix_length = self.__font__.getsize_multiline(self.truncate_suffix)[0]
        while len(self.text) > 1 and self.__font__.getsize_multiline(self.text)[0] + suffix_length >= self.size[0] - error:
            self.text = self.text[0:-1]
        self.text += self.truncate_suffix

    def __pos_from_alignment__ (self):
        width, height = self.__font__.getsize_multiline(self.text)
        x, y = 0, 0
        
        if self.vertical_alignment == "center":
            y = int((self.size[1] / 2) - (height / 2))
        elif self.vertical_alignment == "bottom":
            y = int(self.size[1] - height)

        if self.horizontal_alignment == "center":
            x = int((self.size[0] / 2) - (width / 2))
        elif self.horizontal_alignment == "right":
            x = int(self.size[0] - width)

        return (x, y + paddingcorrection)

    def __wrap_text__ (self):
        self.text = wrap_text_with_font(self.text, self.size[0], self.__font__)

    def __get_font__(self):
        return ImageFont.truetype(path + self.font_family, int(self.font_size))