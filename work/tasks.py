from work_project.celery_app import app
from celery.utils.log import get_task_logger
from work_project.settings import EMAIL_HOST_USER

from django.core.mail import send_mail
from django.utils import timezone

from work.models import (
    Worker, WorkPlace, Statistics,
    APPROVED
)
import datetime
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

    return True


@app.task(name='check_worked_time')  # , queue='mails'
def check_worked_time():

    if not WorkPlace.objects.filter(status=APPROVED).exists():
        return False

    approved_wps = WorkPlace.objects.filter(status=APPROVED)

    from_date = timezone.now() - datetime.timedelta(days=7)

    for wp in approved_wps:
        total_time = 0

        if wp.worktimes.filter(date__gte=from_date).exists():
            week_wts = wp.worktimes.filter(date__gte=from_date)
            
            for wt in week_wts:
                end = wt.time_end.hour + wt.time_end.minute / 60
                start = wt.time_start.hour + wt.time_start.minute / 60
                total_time += end - start

        Statistics.objects.create(
            workplace=wp,
            worker=wp.worker,
            total_worked_time=total_time
        )

        if total_time > wp.week_limit:
            email = wp.manager.email
            subj = 'Worked time is out of week limit'
            msg = (
                f'Worker: {wp.worker.first_name} {wp.worker.last_name}\n'
                f'WorkPlace: {wp.work.name}\n'
                f'Week limit: {wp.week_limit}\n'
                f'Total worked time: {total_time}'
            )
            task = mail_to_manager.delay(subj, msg, email)
            task.get(timeout=10)

    return True


@app.task(name='mail_to_manager', queue='mails')
def mail_to_manager(subj, msg, email):
    send_mail(
        subj,
        msg,
        EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
    return True
