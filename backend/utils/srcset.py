import os

from utils.image import ADAPTIVE_RESOLUTIONS

def get_srcset(url, extension_image):
    path, ext = os.path.splitext(url)
    ext = ext.replace('.', '')
    srcset = ""
    if extension_image != None:
        ext = extension_image
    for resolution in ADAPTIVE_RESOLUTIONS:
        srcset += "{}-{}x{}.{} {}w,".format(path, resolution[0], resolution[1], ext, resolution[0])
    return srcset