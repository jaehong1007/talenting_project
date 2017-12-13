from imagekit import ImageSpec
from imagekit.processors import ResizeToFit


class Thumbnailer(ImageSpec):
    processors = [ResizeToFit(767)]
    format = 'JPEG'
    options = {'quality': 85}
