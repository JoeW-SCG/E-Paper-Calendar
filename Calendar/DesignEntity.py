from PIL import Image, ImageOps, ImageDraw

class DesignEntity (object):
    """General entity that can be drawn on to a panel design or
    other design entities."""
    def __init__ (self, size):
        self.size = size
        self.pos = (0, 0)
        self.__init_image__()
        self.is_bitmap = False

    def __init_image__ (self, color = 'white'):
        self.__image__ = Image.new('L', self.size, color=color)

    def get_image (self):
        self.__finish_image__()
        return self.__image__

    def draw (self, subimage, pos):
        self.__image__.paste(subimage, pos)

    def draw_bitmap (self, subimage, pos):
        ImageDraw.Draw(self.__image__).bitmap(pos, subimage)

    def draw_design (self, entity):
        if entity.is_bitmap:
            self.draw_bitmap(entity.get_image(), entity.pos)
        else:
            self.draw(entity.get_image(), entity.pos)

    def draw_image (self, path, pos):
        self.draw(Image.open(path), pos)

    def __finish_image__ (self):
        pass