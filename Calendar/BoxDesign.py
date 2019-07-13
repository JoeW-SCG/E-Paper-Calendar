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
        topleft = (0, 0)
        bottomright = self.size
        self.corners = [topleft, bottomright]

    def __finish_image__(self):
        ImageDraw.Draw(self.__image__).rectangle(
            self.corners, fill=self.fill, outline=self.outline, width=self.width)
