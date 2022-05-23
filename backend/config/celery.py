import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery('config')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_recipes_of_week_every_week':{
        'task': 'recipes.tasks.send_recipes_of_week_to_subscribers',
        'schedule': crontab(minute="*/5")
    }
}