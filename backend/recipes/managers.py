from django.db.models import Manager
from django.db.models.signals import post_save 


class StepManager(Manager):

    def bulk_create(self, objs, batch_size, ignore_conflicts):
        created_list = super().bulk_create(objs, batch_size, ignore_conflicts)
        for step_object in objs:
            post_save.send(sender=step_object.__class__, instance=step_object)
        return created_list