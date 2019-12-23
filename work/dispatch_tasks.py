from work.tasks import (
    create_workers, mail_to_manager)

 
def manage_create_workers_task(url):
    task = create_workers.delay(url)
    task.get(timeout=5)

manage_create_workers_task('https://jsonplaceholder.typicode.com/users')

def manage_mail_task(email):
    task = mail_to_manager.delay(email)
    task.get(timeout=10)

manage_mail_task('likespony@gmail.com')
