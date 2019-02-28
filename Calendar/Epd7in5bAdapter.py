from EpdAdapter import EpdAdapter, DISPLAY_REFRESH, DATA_START_TRANSMISSION_1
from settings import display_colours
from PIL import Image, ImageDraw

class Epd7in5bAdapter (EpdAdapter):
    def __init__ (self):
        super(Epd7in5bAdapter, self).__init__(384, 640)

    def display_frame (self, frame_buffer):
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(0, int(self.height / 4 * self.width)):
            #the above line had to be modified due to python2 -> python3
            #the issue lies in division, which returns integers in python2
            #but floats in python3
            temp1 = frame_buffer[i]
            j = 0
            while (j < 4):
                if ((temp1 & 0xC0) == 0xC0):
                    temp2 = 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 = 0x00
                else:
                    temp2 = 0x04
                temp2 = (temp2 << 4) & 0xFF
                temp1 = (temp1 << 2) & 0xFF
                j += 1
                if((temp1 & 0xC0) == 0xC0):
                    temp2 |= 0x03
                elif ((temp1 & 0xC0) == 0x00):
                    temp2 |= 0x00
                else:
                    temp2 |= 0x04
                temp1 = (temp1 << 2) & 0xFF
                self.send_data(temp2)
                j += 1
        self.send_command(DISPLAY_REFRESH)
        self.delay_ms(100)
        self.wait_until_idle()

    def get_frame_buffer (self, image):
        buf = [ 0x00 ] * int(self.height * self.width / 4)
        image_rgb = image
        imwidth, imheight = image_rgb.size
        if imwidth != self.height or imheight != self.width:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.height, self.width))

        for y in range(self.width):
            for x in range(self.height):
                # Set the bits for the column of pixels at the current
                # position.
                pixel = image_rgb.getpixel((x, y))
                if self.__brightness__(pixel) < 75: #was 64 # black
                    buf[int((x + y * self.height) / 4)] &= ~(0xC0 >> (x % 4 * 2))
                elif pixel[0] > 150 and (pixel[2] + pixel[1]) < 50:  #was 192
                    buf[int((x + y * self.height) / 4)] &= ~(0xC0 >> (x % 4 * 2))
                    buf[int((x + y * self.height) / 4)] |= 0x40 >> (x % 4 * 2)
                else:                           # white
                    buf[int((x + y * self.height) / 4)] |= 0xC0 >> (x % 4 * 2)
        return buf #due to python2 -> python3, int had to be added in 'get_frame
                   #_buffer

    def __brightness__ (self, pixel):
        return (pixel[0] + pixel[1] + pixel[2]) / 3

    def calibrate (self):
        for _ in range(2):
            self.init_render()
            black = Image.new('1', (self.height, self.width), 'black')
            print('calibrating black...')
            ImageDraw.Draw(black)
            self.display_frame(self.get_frame_buffer(black))

            red = Image.new('L', (self.height, self.width), 'red')
            ImageDraw.Draw(red)
            print('calibrating red...')
            self.display_frame(self.get_frame_buffer(red))

            white = Image.new('1', (self.height, self.width), 'white')
            ImageDraw.Draw(white)
            print('calibrating white...')
            self.display_frame(self.get_frame_buffer(white))
            self.sleep()
        print('Calibration complete')