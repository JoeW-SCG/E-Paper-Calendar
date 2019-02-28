from DisplayAdapter import DisplayAdapter

class ImageFileAdapter (DisplayAdapter):
    """Saves design to an image file, can be used for debugging"""
    def __init__ (self, file_path = ""):
        super(ImageFileAdapter, self).__init__(384, 640)
        self.file_path = file_path

    def render (self, design):
        design.get_image().save(self.file_path + 'design_exported.png')

    def calibrate (self):
        pass