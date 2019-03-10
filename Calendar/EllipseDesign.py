from BoxDesign import BoxDesign
from PIL import ImageDraw, ImageOps

class EllipseDesign (BoxDesign):
    """Redefinition of ImageDraw.Draw.Rectangle"""
    def __init__(self, size, fill=None, outline=None, width=0):
        super(EllipseDesign, self).__init__(size, fill=fill, outline=outline, width=width)

    def __finish_image__ (self):
        ImageDraw.Draw(self.__image__).ellipse(self.corners, fill=self.fill, outline=self.outline, width=self.width)