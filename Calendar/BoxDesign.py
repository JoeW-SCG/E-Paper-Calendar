from DesignEntity import DesignEntity
from PIL import ImageDraw, ImageOps

class BoxDesign (DesignEntity):
    """Redefinition of ImageDraw.Draw.Rectangle"""
    def __init__(self, size, fill=None, outline=None, width=0):
        super(BoxDesign, self).__init__((size[0]+1, size[1]+1), mask=True)
        self.size = size
        self.__define_corners__()
        self.fill = fill
        self.outline = outline
        self.width = width

    def __define_corners__(self):
        topleft = (0,0)
        topright = (self.size[0], 0)
        bottomleft = (0, self.size[1])
        bottomright = self.size
        self.corners = [topleft, topright, bottomright, bottomleft]

    def __finish_image__ (self):
        for i in range(self.width):
            ImageDraw.Draw(self.__image__).polygon(self.__get_reduced_corners__(i), fill=self.fill, outline=self.outline)

    def __get_reduced_corners__(self, reducer):
        topleft = (reducer, reducer)
        topright = (self.size[0] - reducer, reducer)
        bottomleft = (reducer, self.size[1] - reducer)
        bottomright = (self.size[0] - reducer, self.size[1] - reducer)
        return [topleft, topright, bottomright, bottomleft]