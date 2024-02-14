import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'news.tasks.hello',
        'schedule': crontab(hour=11, minute=55, day_of_week='wednesday'),
    },
    'print_one_day': {
        'task': 'news.tasks.printer',
        'schedule': crontab(hour=11, minute=56, day_of_week='wednesday'),
        'args': (5,),
    },
}
