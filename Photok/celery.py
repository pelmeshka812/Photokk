import os
from celery import Celery
from celery.schedules import crontab
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Photok.settings')

app = Celery('Photok')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail': {
        'task': 'accounts.tasks.send_spam',
        'schedule': crontab(minute='*/10'),
    }
}