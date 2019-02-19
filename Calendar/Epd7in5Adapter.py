from EpdAdapter import EpdAdapter, DISPLAY_REFRESH, DATA_START_TRANSMISSION_1
from settings import display_colours
from PIL import Image, ImageDraw

class Epd7in5Adapter (EpdAdapter):
    def __init__ (self):
        super(Epd7in5Adapter, self).__init__(640, 384)

    def display_frame (self, frame_buffer):
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(0, 30720):
            temp1 = frame_buffer[i]
            j = 0
            while (j < 8):
                if(temp1 & 0x80):
                    temp2 = 0x03
                else:
                    temp2 = 0x00
                temp2 = (temp2 << 4) & 0xFF
                temp1 = (temp1 << 1) & 0xFF
                j += 1
                if(temp1 & 0x80):
                    temp2 |= 0x03
                else:
                    temp2 |= 0x00
                temp1 = (temp1 << 1) & 0xFF
                self.send_data(temp2)
                j += 1
        self.send_command(DISPLAY_REFRESH)
        self.delay_ms(100)
        self.wait_until_idle()

    def get_frame_buffer (self, image):
        buf = [0x00] * int(self.width * self.height / 8)
        # Set buffer to value of Python Imaging Library image.
        # Image must be in mode 1.
        image_monocolor = image.convert('1') #with ot withour dithering?
        imwidth, imheight = image_monocolor.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))

        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] != 0:
                    buf[int((x + y * self.width) / 8)] |= 0x80 >> (x % 8)
        return buf

	def calibrate (self):
        for _ in range(2):
            self.init_render()
            black = Image.new('1', (self.width, self.height), 'black')
            print('calibrating black...')
            ImageDraw.Draw(black)
            self.display_frame(self.get_frame_buffer(black))

            white = Image.new('1', (self.width, self.height), 'white')
            ImageDraw.Draw(white)
            print('calibrating white...')
            self.display_frame(self.get_frame_buffer(white))
            self.sleep()
        print('Calibration complete')