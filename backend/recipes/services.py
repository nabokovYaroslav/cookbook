from django.db.models.signals import post_save


def send_post_save_signals(objs):
    for obj in objs:
        old_instance = obj["instance"]
        instance = old_instance.__class__.objects.get(id=old_instance.id)
        sender = instance.__class__
        old_path = obj["old_path"]
        post_save.send(sender=sender, instance=instance, image_was_update=True, old_path=old_path)