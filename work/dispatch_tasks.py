from work.tasks import (
    create_workers,
    check_worked_time,
    mail_to_manager)

 
def manage_create_workers_task(url):
    task = create_workers.delay(url)
    task.get(timeout=5)

def manage_check_time_task():
    task = check_worked_time.delay()
    task.get(timeout=10)

manage_create_workers_task('https://jsonplaceholder.typicode.com/users')
manage_check_time_task()
