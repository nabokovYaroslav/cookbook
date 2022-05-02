import filecmp
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings


def compare_images(existing_image_path : str, image_in_memory: InMemoryUploadedFile):
	path = default_storage.save(image_in_memory.name, ContentFile(image_in_memory.read()))
	tmp_file = os.path.join(settings.MEDIA_ROOT, path)
	equal = False
	if filecmp.cmp(existing_image_path, tmp_file, shallow=False):
		equal = True
	os.remove(tmp_file)
	return equal