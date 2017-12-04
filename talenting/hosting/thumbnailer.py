from imagekit import ImageSpec
from pilkit.processors import ResizeToFill


class Thumbnailer(ImageSpec):
    processors = [ResizeToFill(100, 50)]
    format = 'JPEG'
    options = {'quality': 85}
