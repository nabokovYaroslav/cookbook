from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from recipes.models import Recipe, Step
from utils.image import (change_resolution_of_image, delete_images, create_adaptive_resolution_image, 
                         create_adaptive_format_image) 

@receiver(post_save, sender=Step)
def step_update_image(sender, image_was_update=False, old_path="", **kwargs):
  print(old_path)
  if image_was_update:
    instance = kwargs["instance"]
    print(instance.image.path)
    delete_images(old_path)
    change_resolution_of_image(instance.image.path)
    create_adaptive_resolution_image(instance.image.path, formatting=True)
    create_adaptive_format_image(instance.image.path)

@receiver(post_save, sender=Step)
def step_created(sender, **kwargs):
  instance = kwargs["instance"]
  change_resolution_of_image(instance.image.path)
  create_adaptive_resolution_image(instance.image.path, formatting=True)
  create_adaptive_format_image(instance.image.path)

@receiver(post_delete, sender=Recipe)
def recipe_delete_images(sender, **kwargs):
  instance = kwargs["instance"]
  if instance.image:
    delete_images(instance.image.path)

@receiver(post_delete, sender=Step)
def step_delete_images(sender, **kwargs):
  instance = kwargs["instance"]
  if instance.image:
    delete_images(instance.image.path)