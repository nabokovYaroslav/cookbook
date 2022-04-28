from django.db.models.signals import post_delete
from django.dispatch import receiver

from users.models import User
from utils.image import delete_images

@receiver(post_delete, sender=User)
def user_delete_images(sender, **kwargs):
  instance = kwargs["instance"]
  if instance.image:
    delete_images(instance.image.path)