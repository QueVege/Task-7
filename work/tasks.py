from work_project.celery import app
from celery.utils.log import get_task_logger

from work.models import Worker
import requests
import json


logger = get_task_logger(__name__)

@app.task(name='work.tasks.create_workers')
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
