import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from users.managers import UserManager
from utils.image import (change_resolution_of_image_in_memory, delete_images, create_adaptive_resolution_image, 
                         create_adaptive_format_image, create_tumbnail_image,) 
from utils.file import compare_images


class User(AbstractBaseUser, PermissionsMixin):

  def upload_to(self, file):
    name, ext = os.path.splitext(file)
    path = "images/users/"
    datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
    return output_path

  email = models.EmailField(unique=True)
  user_name = models.CharField(max_length=128, unique=True)
  image = models.ImageField(upload_to=upload_to, default="default/user.png")
  created_at = models.DateTimeField(auto_now=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  objects = UserManager()

  @property
  def is_subscriber(self):
    if(hasattr(self, "subscriber")):
      return True
    return False

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['user_name']

  def save(self, *args, **kwargs):
    is_new_image = False
    try:
      instance = User.objects.get(id=self.id)
    except User.DoesNotExist:
      instance = None
    if instance is not None:
      if not compare_images(instance.image.path, self.image):
        delete_images(instance.image.path)
        self.image = change_resolution_of_image_in_memory(self.image)
        is_new_image = True
      else:
        self.image = instance.image
    else:
      is_new_image = True
      self.image = change_resolution_of_image_in_memory(self.image)
    super().save(*args, **kwargs)
    if is_new_image:
      create_adaptive_resolution_image(self.image.path, formatting=True)
      create_tumbnail_image(self.image.path, formatting=True)
      create_adaptive_format_image(self.image.path)

  def __str__(self):
    return self.user_name
