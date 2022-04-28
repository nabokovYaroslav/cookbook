from django.db.models import Manager
from django.db.models.signals import post_save 


class StepManager(Manager):
    def bulk_update(self, objs, fields, batch_size, step_objects_image_updated=[]):
        count = super().bulk_update(objs, fields, batch_size)
        for step_object in step_objects_image_updated:
            instance = step_object["instance"]
            sender = instance.__class__
            old_path = step_object["old_path"]
            post_save.send(sender, instance, image_was_update=True, old_path=old_path)
        return count

    def bulk_create(self, objs, batch_size, ignore_conflicts):
        created_list = super().bulk_create(objs, batch_size, ignore_conflicts)
        for step_object in objs:
            post_save.send(step_object.__class__, step_object)
        return created_list