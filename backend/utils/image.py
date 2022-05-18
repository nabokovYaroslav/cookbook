import os
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from utils.webp import convert_to_webp


ADAPTIVE_RESOLUTIONS = [
	(540, 540),
	(720, 720),
	(960, 960),
	(1140, 1140),
]

TUMBNAIL_SIZE = 140, 140

MAX_SIZE = max(ADAPTIVE_RESOLUTIONS)

EXTENSIONS = [
	('.webp', convert_to_webp)
]

def change_resolution_of_image_in_memory(image: InMemoryUploadedFile):
	if image:
		im_io = BytesIO()
		im = Image.open(image.file)
		im.thumbnail(MAX_SIZE, Image.ANTIALIAS)
		im.save(im_io, im.format, optimize=True)
		im_file = InMemoryUploadedFile(im_io, None, image.file.name, None, None, None)
		im_io = BytesIO()
		return im_file
	return None

def change_resolution_of_image(image_path: str):
    im = Image.open(image_path)
    im.thumbnail(MAX_SIZE, Image.ANTIALIAS)
    im.save(image_path, optimize=True)

def create_adaptive_resolution_image(image_path, formatting):
	if(os.path.isfile(image_path)):
		path, ext = os.path.splitext(image_path)
		for resolution in ADAPTIVE_RESOLUTIONS:
			file_path = "{}-{}x{}{}".format(path, resolution[0], resolution[1], ext)
			with Image.open(image_path) as im:
				im.thumbnail(resolution, Image.ANTIALIAS)
				im.save(file_path)
			if formatting:
				create_adaptive_format_image(file_path)

def create_adaptive_format_image(image_path):
	if(os.path.isfile(image_path)):
		for extension in EXTENSIONS:
			handler = extension[1]
			handler(image_path)

def crop_center(pil_img, crop_width, crop_height):
	img_width, img_height = pil_img.size
	return pil_img.crop(((img_width - crop_width) // 2,
						 (img_height - crop_height) // 2,
						 (img_width + crop_width) // 2,
						 (img_height + crop_height) // 2))
		
def create_tumbnail_image(image_path, formatting=None):
	if(os.path.isfile(image_path)):
		path, ext = os.path.splitext(image_path)
		file_path = "{}-{}x{}{}".format(path, TUMBNAIL_SIZE[0], TUMBNAIL_SIZE[1], ext)
		with Image.open(image_path) as im:
			im = crop_center(im, min(im.size), min(im.size))
			im.thumbnail(TUMBNAIL_SIZE, Image.ANTIALIAS)
			im.save(file_path)
		if formatting:
			create_adaptive_format_image(file_path)

def delete_images(image_path):
	base_path, ext = os.path.splitext(image_path)
	extensions = [v[0] for v in EXTENSIONS] + [ext]
	resolutions = ADAPTIVE_RESOLUTIONS + [TUMBNAIL_SIZE]
	# delete original image
	for extension in extensions:
		file_path = "{}{}".format(base_path, extension)
		if(os.path.isfile(file_path)):
			os.remove(file_path)
	
	# delete all additional images
	for resolution in resolutions:
		for extension in extensions:
			file_path = "{}-{}x{}{}".format(base_path, resolution[0], resolution[1], extension)
			if(os.path.isfile(file_path)):
				os.remove(file_path)

def get_adaptive_image(url, extension_image):
    if extension_image == None:
        return url
    path, ext = os.path.splitext(url)
    ext = extension_image
    return "{}.{}".format(path, ext)

def get_tumbnail(url, extension_image):
	path, ext = os.path.splitext(url)
	ext = ext.replace(".", "")
	if extension_image is not None:
		ext = extension_image
	return "{}-{}x{}.{}".format(path, TUMBNAIL_SIZE[0], TUMBNAIL_SIZE[1], ext)