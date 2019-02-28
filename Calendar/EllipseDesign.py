from BoxDesign import BoxDesign
from PIL import ImageDraw, ImageOps

class EllipseDesign (BoxDesign):
    """Redefinition of ImageDraw.Draw.Rectangle"""
    def __init__(self, size, fill=None, outline=None, width=0):
        super(EllipseDesign, self).__init__(size, fill=fill, outline=outline, width=width)

    def __finish_image__ (self):
        for i in range(self.width):
            corners = self.__get_reduced_corners__(i)
            ImageDraw.Draw(self.__image__).ellipse([corners[0], corners [2]], fill=self.fill, outline=self.outline)
        self.__image__ = ImageOps.invert(self.__image__)