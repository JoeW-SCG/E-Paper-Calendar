from PanelDesign import PanelDesign
from settings import general_settings
from Assets import supported_img_formats, path as application_path
from os import listdir
from os.path import isfile, join
from ImageDesign import ImageDesign
from random import choice


class ImageFramePanel (PanelDesign):
    """Converts the display into a digital frame and
    shows a slide show of images, iterating on each update"""
    def __init__ (self, size):
        super(ImageFramePanel, self).__init__(size)
        self.overlay_path = self.__complete_path__(general_settings["overlay-image"])
        self.image_folder_path = self.__complete_path__(general_settings["image-folder"])
        self.images = self.__extract_valid_img_paths__()
        self.__first_render__()

    def __extract_valid_img_paths__ (self):
        images = []
        for file in listdir(self.image_folder_path):
            file_path = join(self.image_folder_path, file).replace('\\', '/')
            if isfile(file_path) and self.overlay_path != file_path:
                if file.split('.')[-1].upper() in supported_img_formats:
                    images.append(file_path)
        return images

    def __complete_path__(self, path):
        path = path.replace('\\', '/')
        if path[0] != '/' and ':' not in path[0:3]:
            path = join(application_path, path)
        return path

    def __first_render__(self):
        current_image = choice(self.images)
        img = ImageDesign(self.size, current_image, fill="scale", color="1")
        self.draw_design(img)

        if self.overlay_path != "":
            overlay = ImageDesign(self.size, self.overlay_path)
            overlay.__finish_image__()
            self.__image__.alpha_composite(overlay.__image__)

    def add_weather (self, weather):
        pass

    def add_calendar (self, calendar):
        pass

    def add_rssfeed (self, rss):
        pass

    def add_crypto (self, crypto):
        pass

    def add_tasks (self, tasks):
        pass
