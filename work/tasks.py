from work_project.celery_app import app
from celery.utils.log import get_task_logger
from work_project.settings import EMAIL_HOST_USER

from django.core.mail import send_mail

from work.models import Worker
import requests
import json


logger = get_task_logger(__name__)

@app.task(name='create_workers', queue='working')
def create_workers(url):
    connect_timeout, read_timeout = 5.0, 30.0
    response = requests.get(
        url,
        timeout=(connect_timeout, read_timeout)
    )
    users_data = response.json()

    counter = 0

    for user in users_data:
        name = user['name'].split(' ')
        first_n = name[0]
        last_n = ' '.join(name[1::])

        if not Worker.objects.filter(first_name=first_n).filter(last_name=last_n).exists():
            Worker.objects.create(
                first_name=first_n,
                last_name=last_n
            )
            counter += 1

    logger.info(f'{counter} workers was successfully added')


# @app.task(name='check_overworking', queue='working')
# def create_workers(url):
#     pass


@app.task(name='mail_to_manager', queue='mails')
def mail_to_manager(email):
    send_mail(
        'Hello',
        'Can you see me?',
        EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
