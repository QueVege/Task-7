from work_project.celery import app
from work.models import Worker
import requests
import json

@app.task(name='work.tasks.create_workers')
def create_workers():
    connect_timeout, read_timeout = 5.0, 30.0
    response = requests.get(
        'https://jsonplaceholder.typicode.com/users',
        timeout=(connect_timeout, read_timeout)
    )
    users_data = response.json()

    for user in users_data:
        name = user['name'].split(' ')
        first_n = name[0]
        last_n = ' '.join(name[1::]

        if not Worker.objects.filter(
            first_name=first_n).filter(last_name=last_n).exists():
    
            Worker.objects.create(
                first_name=first_n,
                last_name=last_n
            )
    