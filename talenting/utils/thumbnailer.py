from easy_thumbnails.files import get_thumbnailer


def customThumbnailer(img):
    if img:
        thumbnail_options = dict(size=(100, 0))
        file = get_thumbnailer(img).get_thumbnail(thumbnail_options)
        return file
