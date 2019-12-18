import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'work_project.settings')

app = Celery('work_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
